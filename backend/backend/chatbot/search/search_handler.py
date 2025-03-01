from os import path
import pickle
import pandas as pd
from typing import cast, Sequence, Any
from enum import Enum
from ..confirmation.confirmation_classifier import confirmation_classifier
from ..utils.corpus_processor import CorpusProcessor
from ..utils.protocols.handler import Handler
from ..utils.find_max_similarity import find_max_similarity
from ..utils.aggregate import aggregate
from ..utils.errors import IntentNotFoundError
import numpy.typing as npt
import numpy as np
from utils.chatbot_use_cases import ChatbotUseCases
from entities.user import UserEntity
from dtos.track import Track, Tracks

class _FollowupType(str, Enum):
    InitSearch = 'InitSearch'
    SearchByName = 'SearchByName'
    SearchByGenre = 'SearchByGenre'
    AddArtists = 'AddArtists'
    AddMoreSongs = 'AddMoreSongs'

class _IntentType(str, Enum):
    NextPage = 'NextPage'
    PrevPage = 'PrevPage'
    First = 'First'
    Second = 'Second'
    Third = 'Third'
    Fourth = 'Fourth'
    Fifth = 'Fifth'

class SearchHandler(Handler):
    key = 'search'
    _min_similarity = 0.65
    _min_no_confirmation_similarity = 0.8

    _non_initial_intents = [
        _FollowupType.SearchByName,
        _FollowupType.SearchByGenre,
        _FollowupType.AddArtists,
        _FollowupType.AddMoreSongs,
        _IntentType.PrevPage,
        _IntentType.NextPage,
        _IntentType.First,
        _IntentType.Second,
        _IntentType.Third,
        _IntentType.Fourth,
        _IntentType.Fifth,
    ]

    def __init__(
        self,
        state: dict[str, Any] | None,
        user: UserEntity,
        spotify_playlist_id: str,
        use_cases: ChatbotUseCases,
    ):
        self._base_path = path.dirname(__file__)
        self._dataset, self._processor, self._doc_term_matrix = self._load_model()
        self._state = state or {}
        self._user = user
        self.spotify_playlist_id = spotify_playlist_id
        self._use_cases = use_cases

    def match_intent(self, query: str, only: Sequence[str] = []):
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

        entry = self._dataset.iloc[index]
        intent_type = cast(str, entry['FollowupType'])
        if len(only) != 0 and intent_type not in only:
            # These queries aren't meant to be matched outside of specific scenarios
            return None

        self._state['index'] = index
        self._state['similarity'] = similarity

        return similarity

    async def generate_initial_response(self):
        similarity = cast(float, self._state['similarity'])
        index = cast(int, self._state['index'])

        if similarity >= self._min_no_confirmation_similarity:
            response = self._get_initial_response()

            return response, False
        elif similarity >= self._min_similarity:
            self._state['index'] = index
            self._state['from_confirmation'] = True
            question = self._dataset.iloc[index]['Question']
            response = f"I'm sorry, I didn't quite understand that. Did you mean \"{question}\"?"
            return response, False

        raise IntentNotFoundError

    async def generate_followup_response(self, query: str):
        if self._state.get('from_confirmation'):
            if confirmation_classifier.predict(query):
                response = self._get_initial_response()
                is_finished = False
            else:
                response = "My apologies for misunderstanding your query. Can you please rephrase it?"
                is_finished = True

            del self._state['index'], self._state['similarity'], self._state['from_confirmation']
        else:
            response, is_finished = await self._get_followup_response(query)

        return response, is_finished

    def export_state(self):
        return self._state

    def _load_model(self):
        model_path = path.join(self._base_path, 'search_model.pickle')

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
        dataset = pd.read_csv(path.join(self._base_path, 'search_dataset.csv'))
        processor = CorpusProcessor()
        questions = cast(npt.NDArray[np.str_], dataset['Question'].values)
        doc_term_matrix = processor.fit_transform(questions)

        return dataset, processor, doc_term_matrix

    def _get_initial_response(self):
        index = cast(int, self._state['index'])
        entry = self._dataset.iloc[index]
        followup_type = cast(_FollowupType, entry['FollowupType'])
        self._state['followup_type'] = followup_type

        return cast(str, entry['Response'])

    async def _get_followup_response(self, query: str) -> tuple[str, bool]:
        match self._state.get('followup_type'):
            case _FollowupType.InitSearch:
                return await self._handle_init_search(query)
            case _FollowupType.SearchByName | _FollowupType.SearchByGenre:
                self._state['search_query'] = query
                self._state['search_type'] = cast(_FollowupType, self._state['followup_type'])

                entry = self._dataset[self._dataset['FollowupType'] == _FollowupType.AddArtists]
                self._state['index'] = int(cast(np.int64, entry.index[0]))
                return self._get_initial_response(), False
            case _FollowupType.AddArtists:
                self._state['artists'] = query
                self._state['page'] = 1
                del self._state['followup_type']
                return await self._handle_search(), False
            case _FollowupType.AddMoreSongs:
                if not confirmation_classifier.predict(query):
                    return 'Ok.', True

                tracks = Tracks.model_validate(self._state['search_results']).tracks
                return self._realise_search_results(tracks), False
            case _:
                pass

        selected = 0
        response = ''

        if query in ['1', '2', '3', '4', '5']:
            selected = int(query)
        else:
            intents = [
                _IntentType.PrevPage,
                _IntentType.NextPage,
                _IntentType.First,
                _IntentType.Second,
                _IntentType.Third,
                _IntentType.Fourth,
                _IntentType.Fifth,
            ]
            similarity = self.match_intent(query, intents)
            if similarity == None:
                raise IntentNotFoundError

            index = cast(int, self._state['index']) # index is set by match_intent
            entry = self._dataset.iloc[index]
            page = cast(int, self._state['page'])

            match entry['FollowupType']:
                case _IntentType.PrevPage:
                    if page == 1:
                        response = 'You are already at the first page'

                    self._state['page'] = page - 1
                    response = await self._handle_search()
                case _IntentType.NextPage:
                    self._state['page'] = page + 1
                    response = await self._handle_search()
                case _IntentType.First:
                    selected = 1
                case _IntentType.Second:
                    selected = 2
                case _IntentType.Third:
                    selected = 3
                case _IntentType.Fourth:
                    selected = 4
                case _IntentType.Fifth:
                    selected = 5
                case _:
                    raise IntentNotFoundError

        if selected != 0:
            response = await self._handle_add_to_playlist(selected)

        return response, False

    def _handle_init_search(self, query: str):
        similarity = self.match_intent(
            query,
            [_FollowupType.SearchByName, _FollowupType.SearchByGenre],
        )

        if not similarity or similarity <= self._min_no_confirmation_similarity:
            raise IntentNotFoundError

        return self.generate_initial_response()

    async def _handle_search(self):
        match self._state['search_type']:
            case _FollowupType.SearchByGenre:
                search_type = 'genre'
            case _FollowupType.SearchByName:
                search_type = 'name'
            case _:
                raise ValueError('Invalid search type')

        search_query = cast(str, self._state['search_query'])
        artists = cast(str, self._state['artists'])
        page = cast(int, self._state['page'])

        search_results = await self._use_cases.search_tracks_use_case.execute(
            self._user,
            search_query,
            search_type,
            artists,
            page,
        )
        self._state['search_results'] = search_results.as_tracks.model_dump()
        return self._realise_search_results(search_results.as_tracks.tracks)

    def _realise_search_results(self, results: list[Track]):
        page = cast(int, self._state['page'])
        if len(results) == 0:
            if self._state['page'] != 1:
                # if results is empty and it is not the first page, that means there's no more result
                self._state['page'] = page - 1
                return 'No more results.'

            # otherwise, there is no results found
            return 'No results found.'

        response = f'Here is page {page} of the results I found:\n\n'
        for index, track in enumerate(results):
            artists = self._aggregate_artists(track.artists)
            response += f'{index + 1}.\n{track.name} by {artists}\n\n'

        if len(results) < 5:
            response += "You've reached the end of the search results.\n"
            if page != 1:
                response += 'You can navigate the search results with "previous page"\n\n'

        if page != 1:
            response += 'You can navigate the search results with "next page" or "previous page"\n\n'
        else:
            response += 'You can navigate the search results with "next page"\n\n'

        response += 'Which one would you like to add to your playlist? (1 ~ 5)'

        return response

    def _aggregate_artists(self, artists: list[str]):
        return '' if len(artists) == 0 else aggregate(artists)

    async def _handle_add_to_playlist(self, position: int):
        if 'search_results' not in self._state:
            raise IntentNotFoundError

        tracks = Tracks.model_validate(self._state['search_results']).tracks
        index = position - 1
        track = tracks[index]

        await self._use_cases.add_tracks_to_playlist_use_case.execute(
            self._user,
            self.spotify_playlist_id,
            [track.uri],
        )

        self._state['followup_type'] = _FollowupType.AddMoreSongs

        artists = self._aggregate_artists(track.artists)
        response = f'Done! {track.name} by {artists} has been added to your playlist.\n'
        response += 'Would you like to add more from the current search results?'

        return response
