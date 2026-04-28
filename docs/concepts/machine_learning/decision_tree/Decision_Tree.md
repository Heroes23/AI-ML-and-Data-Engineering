## Decision Tree Guide

### Table of Contents

- [Entropy Calculation](./Entropy.md)
- [Gini Impurity Calculation](./Gini_Impurity.md)
- [Information Gain]()
- [Learning Objective - Classification](./Learning_Objective_Classification.md)
- [Learning Objective - Regression]()

### Description


## Python Example

```python
import numpy as np

# Build a class
class DecisionTree:

    # Constructor
    def __init__(self, max_depth: int = 5, min_samples_split: int = 2):

        # Attributes
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split

        # Separate attribute to refer to our tree
        self.tree = None
    
    # Criterion - Gini Impurity
    def gini(self, y: np.ndarray):

        # Classes and their frequenceis
        classes, counts = np.unique(y, return_counts=True)

        # Probabilities
        probs = counts / len(y)

        return 1 - np.sum(probs ** 2)
    
    # Best Split
    def best_split(self, X: np.ndarray, y: np.ndarray):
        """
        
        ### Inputs
        - X (2D numpy array):
            - 1st dimension:  Samples of data (Rows)
            - 2nd dimension : Features (Columns)
        
        - y (1D numpy array):
            - Output labels (Classification)
        
        """
        # Best feature, best threshold
        best_feature, best_thres = None, None

        # Best impurity
        best_impurity = np.inf

        # Parent's impurity
        parent_impurity = self.gini(y=y)

        # Break up the input into samples and features
        n_samples, n_features = X.shape

        # Go through each feature
        for feature in range(n_features):

            # Develop thresholds
            thresholds = np.unique(X[:, feature])

            # Go through each of thresholds
            for thres in thresholds:

                # Indices
                left_idx = X[:, feature] <= thres
                right_idx = ~left_idx

                # Length of the outcome variable when you split on the indices
                if len(y[left_idx]) < self.min_samples_split or len(y[right_idx]) < self.min_samples_split:
                    continue

                # Calculate impurities
                left_imp = self.gini(y[left_idx])
                right_imp = self.gini(y[right_idx])

                # Weighted Impurities
                weighted_imp = (
                    len(y[left_idx]) * left_imp + len(y[right_idx]) * right_imp
                ) / n_samples

                # Check if the weighted impurity is less than your best impurity
                if weighted_imp < best_impurity:
                    # Reassign some values
                    best_impurity = weighted_imp
                    best_feature = feature
                    best_thres = thres
        
        return best_feature, best_thres
    
    # build the tree
    def build_tree(self, X, y, depth):

        # Stopping conditions
        if depth > self.max_depth or len(y) < self.min_samples_split:
            return self.leaf_value(y)

        feature, thres = self.best_split(X, y)

        # Don't have a split
        if feature is None:
            return self.leaf_value(y)
        
        # Construct left and right indices
        left_idx = X[:, feature] <= thres
        right_idx = ~left_idx

        # Subtrees
        left_subtree = self.build_tree(X[left_idx], y[left_idx], depth + 1)
        right_subtree = self.build_tree(X[right_idx], y[right_idx], depth+1)

        return (feature, thres, left_subtree, right_subtree)
    
    def leaf_value(self, y):
        values, counts = np.unique(y, return_counts=True)

        return values[np.argmax(counts)]
    
    def fit(self, X, y):
        X = np.array(X)
        y = np.array(y)
        self.tree = self.build_tree(X, y, 0)
    
    def predict_one(self, x, tree):

        if not isinstance(tree, tuple):
            return tree

        feature, thres, left, right = tree

        if x[feature] <= thres:
            return self.predict_one(x, left)
        
        else:
            return self.predict_one(x, right)
    
    def predict(self, X):
        X = np.array(X)

        return np.array([self.predict_one(x, self.tree) for x in X])
    

# Usage
X = np.array([
    [2,3],
    [1,1],
    [3,4],
    [5,2],
    [4,2]
])

y = np.array([0,0,0,1,1])

# Build the tree
tree = DecisionTree(max_depth=3)

# Fitting the tree
tree.fit(X, y)

# predictions
print(tree.predict([[3,2], [1,2]]))

```


## Scikit Learn

```python

import numpy as np
from sklearn.tree import DecisionTreeClassifier

# Decision Tree
dt = DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=3)

# Usage
X = np.array([
    [2,3],
    [1,1],
    [3,4],
    [5,2],
    [4,2]
])

y = np.array([0,0,0,1,1])

dt.fit(X, y)

X_test = [[3,2], [1,2]]

y_pred = dt.predict(X_test)

print(y_pred)

```