import numpy as np

class TreeNode:
    def __init__(self,
        feature_index=None,
        threshold=None,
        left=None,
        right=None,
        value=None):

        # Attributes
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value  # leaf value (float)

    # Determines if the node is a leaf node
    def is_leaf(self):
        return self.value is not None

class RegressionTree:

    # Constructor
    def __init__(self,
        max_depth: int = 3,
        min_samples_split: int = 2,
        criterion: str = 'mse'):
        """
        Regression Tree with configurable loss criterion.

        Parameters:
        -----------
        max_depth : int
            Maximum depth of the tree
        min_samples_split : int
            Minimum number of samples required to split a node
        criterion : str
            Loss function to use for splits. Options: 'mse' or 'sse'
            - 'mse': Mean Squared Error (default)
            - 'sse': Sum of Squared Errors
        """

        # Attributes
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.criterion = criterion.lower()

        if self.criterion not in ['mse', 'sse']:
            raise ValueError("criterion must be either 'mse' or 'sse'")

        self.root = None

    def _calculate_loss(self, y_left, y_right, n_samples):
        """
        Calculate loss based on the selected criterion.

        Parameters:
        -----------
        y_left : array
            Target values in left split
        y_right : array
            Target values in right split
        n_samples : int
            Total number of samples in parent node

        Returns:
        --------
        float
            Calculated loss value
        """
        if self.criterion == 'mse':
            # Mean Squared Error (weighted variance)
            loss = (
                y_left.var() * len(y_left) + y_right.var() * len(y_right)
            ) / n_samples
        else:  # sse
            # Sum of Squared Errors
            sse_left = np.sum((y_left - np.mean(y_left))**2)
            sse_right = np.sum((y_right - np.mean(y_right))**2)
            loss = sse_left + sse_right

        return loss

    # Fit method
    def fit(self, X, y):
        X = np.asarray(X)
        y = np.asarray(y)

        # Build root
        self.root = self._build_tree(X, y, depth=0)

    # Build the tree
    def _build_tree(self, X, y, depth):
        n_samples, n_features = X.shape

        # Stopping Conditions
        if (depth >= self.max_depth or n_samples < self.min_samples_split or np.unique(y).shape[0] == 1):

            # Assign the leaf value as mean of all the residuals in sample
            leaf_value = float(np.mean(y))

            return TreeNode(value=leaf_value)

        # If no stopping condition met:
        best_feat, best_thresh, best_loss = None, None, np.inf

        for feature_index in range(n_features):
            x_col = X[:, feature_index]
            unique_vals = np.unique(x_col)

            if unique_vals.shape[0] == 1:
                continue

            thresholds = (unique_vals[:-1] + unique_vals[1:]) / 2.0

            # Iterate through thresholds
            for t in thresholds:
                left_mask = x_col <= t
                right_mask = ~left_mask

                if left_mask.sum() == 0 or right_mask.sum() == 0:
                    continue

                y_left = y[left_mask]
                y_right = y[right_mask]

                # Calculate loss using the selected criterion
                loss = self._calculate_loss(y_left, y_right, n_samples)

                if loss < best_loss:
                    best_loss = loss
                    best_feat = feature_index
                    best_thresh = float(t)

        if best_feat is None:
            # Get the mean of all values
            return TreeNode(value=float(np.mean(y)))

        # Update masks
        left_mask = X[:, best_feat] <= best_thresh
        right_mask = ~left_mask

        # Update children
        left_child = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_child = self._build_tree(X[right_mask], y[right_mask], depth + 1)

        # Build the new TreeNode
        return TreeNode(
            feature_index=best_feat,
            threshold=best_thresh,
            left=left_child,
            right=right_child

        )

    # Predict a sample
    def predict_sample(self, x, node):
        if node.is_leaf():
            return node.value

        if x[node.feature_index] <= node.threshold:
            return self.predict_sample(x, node.left)
        else:
            return self.predict_sample(x, node.right)

    # Overall predict function
    def predict(self, X):
        X = np.asarray(X)

        return np.array([self.predict_sample(x, self.root) for x in X], dtype=float)


# Example usage demonstrating both criteria
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    X = np.random.rand(100, 2) * 10
    y = 2 * X[:, 0] + 3 * X[:, 1] + np.random.randn(100) * 2

    # Train with MSE
    print("Training with MSE criterion:")
    tree_mse = RegressionTree(max_depth=3, criterion='mse')
    tree_mse.fit(X, y)
    predictions_mse = tree_mse.predict(X[:5])
    print(f"Predictions (MSE): {predictions_mse}")
    print(f"Actual values: {y[:5]}\n")

    # Train with SSE
    print("Training with SSE criterion:")
    tree_sse = RegressionTree(max_depth=3, criterion='sse')
    tree_sse.fit(X, y)
    predictions_sse = tree_sse.predict(X[:5])
    print(f"Predictions (SSE): {predictions_sse}")
    print(f"Actual values: {y[:5]}")
