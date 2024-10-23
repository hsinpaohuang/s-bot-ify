from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from typing import cast
import numpy.typing as npt
import numpy as np

class CorpusProcessor():
    def __init__(self):
        self._analyser = CountVectorizer().build_analyzer()
        self._processor = CountVectorizer(analyzer=self._analyse)
        self._transformer = TfidfTransformer()

        self._lemmatiser = WordNetLemmatizer()
        self._POSMAP = { 'ADJ': 'a', 'ADV': 'r', 'NOUN': 'n', 'VERB': 'v' }
        self._POSMAP_KEYS = set(self._POSMAP.keys())

    def fit_transform(self, corpus: list[str] | npt.NDArray[np.str_]):
        count = self._processor.fit_transform(corpus)
        return cast(npt.NDArray[np.float64], self._transformer.fit_transform(count))

    def transform(self, query: str):
        count = self._processor.transform([query])
        return self._transformer.transform(count)

    def _analyse(self, doc: str):
        tokenised = cast(list[str], self._analyser(doc))
        return self._lemmatise(tokenised)

    def _lemmatise(self, tokenised_doc: list[str]):
        tagged = cast(list[tuple[str, str]], pos_tag(tokenised_doc, tagset='universal'))
        output = list[str]()

        for token, tag in tagged:
            if tag in self._POSMAP_KEYS:
                lemmatised_token = self._lemmatiser.lemmatize(token, self._POSMAP[tag])
            else:
                lemmatised_token = self._lemmatiser.lemmatize(token)
            output.append(lemmatised_token)

        return output
