from os import path
import pickle
import pandas as pd
from typing import cast, Any
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression

class _ConfirmationClassifier():
    def __init__(self):
        self._base_path = path.dirname(__file__)
        self._classifier, self._vectoriser, self._transformer = self._load_model()

    def _load_model(self):
        model_path = path.join(self._base_path, 'confirmation_model.pickle')
        if path.isfile(model_path):
            with open(model_path, 'rb') as file:
                return pickle.load(file)

        model = self._train()
        with open(model_path, 'wb') as file:
            pickle.dump(model, file)

        return model

    def predict(self, query: str) -> bool:
        """
        Predicts if the given query is positive or negative in a yes-or-no question

        :param query: user's input

        :returns: result
            True if the user means 'yes', False if the user means 'no'
        """

        count = self._vectoriser.transform([query.lower()])
        transformed = self._transformer.transform(count)
        predicted = self._classifier.predict(transformed)

        return predicted[0] == 'positive'

    def _train(self, classifier: Any = LogisticRegression):
        # reference: Lab 3 part 5 & 6

        positives_path = path.join(self._base_path, 'positives.csv')
        negatives_path = path.join(self._base_path, 'negatives.csv')
        positives = cast(list[str], pd.read_csv(positives_path)['Query'].to_list())
        negatives = cast(list[str], pd.read_csv(negatives_path)['Query'].to_list())

        data = positives + negatives
        labels = ['positive' for _ in positives] + ['negative' for _ in negatives]

        X_train, _X_test, y_train, _y_test = train_test_split(
            data,
            labels,
            stratify=labels,
            test_size=0.25,
            random_state=9,
        )

        vectoriser = CountVectorizer()
        X_train_counts = vectoriser.fit_transform(X_train)
        transformer = TfidfTransformer().fit(X_train_counts)

        classifier = LogisticRegression(random_state=0).fit(transformer.transform(X_train_counts), y_train)

        return classifier, vectoriser, transformer

confirmation_classifier = _ConfirmationClassifier()
