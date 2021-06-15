class BaseActiveLearningComponent:

    def fit(self, X, y):
        """
        Fits the estimator and returns a reference to itself.
        """
        return self

    def partial_fit(self, X, y):
        """
        Updates the estimator given the data X, y.
        Returns a reference to itself.
        """
        return self

    def rank(self, X):
        """
        Ranks the instances in X.
        Returns a list of indices, sorted by relevance.
        The first index points to the most useful instance.
        """
        return None
