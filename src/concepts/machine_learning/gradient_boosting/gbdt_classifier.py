import numpy as np

# Import the Regression Tree
from regression_tree import RegressionTree

# Sigmoid Function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class GradientBoostedClassifier:
    """
    Binary GBM classifier with log loss.
    - y in {0,1}
    - F(x) is log-odds; p = sigmoid(F)
    - pseudo-residual = y - p (negative gradient)
    """
    def __init__(self, n_estimators=50, learning_rate=0.1,
                 max_depth=3, min_samples_split=2):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.init_score_ = None
        self.trees_ = []

    def _init_score(self, y):
        # initial log-odds: log(p / (1-p))
        p = np.clip(np.mean(y), 1e-6, 1 - 1e-6)
        return float(np.log(p / (1 - p)))

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        assert set(np.unique(y)).issubset({0.0, 1.0}), "Labels must be 0/1."

        self.init_score_ = self._init_score(y)
        F = np.full_like(y, self.init_score_, dtype=float)  # current scores
        self.trees_ = []

        for m in range(self.n_estimators):
            p = sigmoid(F)
            residual = y - p  # negative gradient

            tree = RegressionTree(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split
            )
            tree.fit(X, residual)
            update = tree.predict(X)

            F += self.learning_rate * update
            self.trees_.append(tree)

    def _decision_function(self, X):
        X = np.asarray(X, dtype=float)
        F = np.full(X.shape[0], self.init_score_, dtype=float)
        for tree in self.trees_:
            F += self.learning_rate * tree.predict(X)
        return F

    def predict_proba(self, X):
        F = self._decision_function(X)
        p = sigmoid(F)
        return np.vstack([1 - p, p]).T

    def predict(self, X):
        proba = self.predict_proba(X)[:, 1]
        return (proba >= 0.5).astype(int)