class BaseActiveLearningComponent:

    def fit(self, X, y):
        """
        Fits the estimator and returns a reference to itself
        """
        return self

    def partial_fit(self, X, y):
        """
        Updates the estimators params given the data X, y.
        Returns a reference to itself
        """
        return self

    def rank(self, X):
        """
        Ranks the instances in X in terms of its active learning strategy.
        Returns a list of indices where the first indices is points to the most useful instance
        """
        return None
