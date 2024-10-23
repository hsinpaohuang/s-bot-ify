from os import path
import pickle
import pandas as pd
from enum import Enum
from typing import cast, Any
import numpy.typing as npt
import numpy as np
from ..confirmation.confirmation_classifier import confirmation_classifier
from ..utils.corpus_processor import CorpusProcessor
from ..utils.protocols.handler import Handler
from ..utils.find_max_similarity import find_max_similarity
from ..utils.errors import IntentNotFoundError

class _IntentType(str, Enum):
    Greeting = 'Greeting'
    Help = 'Help'

class SmalltalkHandler(Handler):
    key = 'smalltalk'
    _min_similarity = 0.65
    _min_no_confirmation_similarity = 0.8

    def __init__(self, state: dict[str, Any] | None):
        self._base_path = path.dirname(__file__)
        self._dataset, self._processor, self._doc_term_matrix = self._load_model()
        self._state = state or {}

    def match_intent(self, query: str):
        transformed = self._processor.transform(query)
        flattened = cast(npt.NDArray[np.float64], transformed.toarray().flatten()) # pyright: ignore
        if np.sum(flattened) == 0:
            # none of the tokens in query is in the vocab, so no entry can be matched
            return None

        index, similarity = find_max_similarity(self._doc_term_matrix, flattened)

        # if similarity is smaller than the arbitrary threshold,
        # then the similarity is too low to be considered valid
        if similarity < self._min_similarity:
            return None

        self._state['index'] = index
        self._state['similarity'] = similarity

        return similarity

    async def generate_initial_response(self):
        similarity = cast(float, self._state['similarity'])
        index = cast(int, self._state['index'])

        if similarity >= self._min_no_confirmation_similarity:
            response, is_finished = self._get_response()
            del self._state['similarity']

            return response, is_finished

        if similarity >= self._min_similarity:
            self._state['index'] = index
            self._state['from_confirmation'] = True
            question = self._dataset.iloc[index]['Question']
            response = f"I'm sorry, I didn't quite understand that. Did you mean \"{question}\"?"

            return response, False

        raise IntentNotFoundError

    def generate_followup_response(self, query: str):
        if self._state.get('from_confirmation'):
            if confirmation_classifier.predict(query):
                response, is_finished = self._get_response()
            else:
                response = "My apologies for misunderstanding your query. Can you please rephrase it?"
                is_finished = True

            del self._state['similarity'], self._state['from_confirmation']
        else:
            raise IntentNotFoundError

        return response, is_finished

    def export_state(self):
        return self._state

    def _load_model(self):
        model_path = path.join(self._base_path, 'smalltalk_model.pickle')

        if path.isfile(model_path):
            with open(model_path, 'rb') as f:
                model = cast(
                    tuple[pd.DataFrame, CorpusProcessor, npt.NDArray[np.float64]],
                    pickle.load(f),
                )
        else:
            model = self._initialise_model()
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)

        return model

    def _initialise_model(self):
        dataset = pd.read_csv(path.join(self._base_path, 'smalltalk_dataset.csv'))
        processor = CorpusProcessor()
        questions = cast(npt.NDArray[np.str_], dataset['Question'].values)
        doc_term_matrix = processor.fit_transform(questions)

        return dataset, processor, doc_term_matrix

    def _get_response(self):
        index = cast(int, self._state['index'])

        entry = self._dataset.iloc[index]
        response = cast(str, entry['Response'])

        if entry['IntentType'] == _IntentType.Help:
            entry = self._dataset[self._dataset['QuestionID'] == 15].iloc[0] # QuestionID for help message
            response = cast(str, entry['Response'])

        return response, True
