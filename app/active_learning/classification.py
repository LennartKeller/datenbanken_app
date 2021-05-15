import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import make_pipeline

from app.active_learning.base_estimator import BaseActiveLearningComponent


class LogRegUncertainty(BaseActiveLearningComponent):

    def __init__(self):
        self.pipeline = make_pipeline(
            TfidfVectorizer(stop_words='english', max_features=5000),
            SGDClassifier(loss='log', penalty='l2', random_state=42)
        )

    def fit(self, X, y):
        """
        X: List of texts,
        y: List of labels (str) for each text
        """
        self.pipeline.fit(X, y)

    def rank(self, X):
        probs = self.pipeline.predict_proba(X)
        return self.margin_sampling(probs)

    @staticmethod
    def margin_sampling(y_probs: np.array):
        """
        Formula: x_m = argmin(x) P(y_1, x) - P(y_2, x)
            where y_1 = Most probable class of x, y_2 second most probable class of x

        """
        y_probs_2_max = []
        for probas in y_probs:
            # get indices of max 2 probs
            ind = np.argpartition(probas, -2)[-2:]
            # subtract max prob from second max probs
            y_probs_2_max.append(probas.item(ind.item(1)) - probas.item(ind.item(0)))
        y_probs_2_max = np.array(y_probs_2_max)
        min_ind = y_probs_2_max.argsort()
        return min_ind
