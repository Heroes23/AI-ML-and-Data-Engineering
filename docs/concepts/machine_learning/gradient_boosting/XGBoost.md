## XGBoost (Extreme Gradient Boosting)

### Topics

1. What is XGBoost?
2. Key Innovations Over Standard GBDT
3. Regularized Objective Function
4. Second-Order Approximation
5. Tree Structure Score
6. Split Finding Algorithm
7. Python Implementation - From Scratch
8. Python Implementation - Using XGBoost Library

### What is XGBoost?

- XGBoost stands for **Extreme Gradient Boosting** and is an optimized implementation of gradient boosted decision trees.

- It was developed by Tianqi Chen in 2014 and has become one of the most popular machine learning algorithms for structured/tabular data.

- XGBoost builds upon the foundation of gradient boosting but adds several key innovations:
    - **Regularization**: Penalizes model complexity to prevent overfitting
    - **Second-order approximation**: Uses both first and second derivatives of the loss function
    - **Efficient computation**: Optimized algorithm for finding best splits
    - **Built-in cross-validation**: Easy hyperparameter tuning
    - **Handling missing values**: Automatic handling of sparse data
    - **Parallel processing**: Can utilize multiple CPU cores

### Key Innovations Over Standard GBDT

#### 1. Regularized Objective Function

- Standard GBDT only minimizes the loss function
- XGBoost adds a regularization term to control model complexity

$$ \text{Obj} = \sum_{i=1}^{n} L(y_i, \hat{y}_i) + \sum_{k=1}^{K} \Omega(f_k) $$

Where:
- $L(y_i, \hat{y}_i)$ is the loss function (e.g., log loss for classification)
- $\Omega(f_k)$ is the regularization term for tree $k$
- $K$ is the number of trees

#### 2. Second-Order Taylor Expansion

- Standard GBDT uses only the first derivative (gradient)
- XGBoost uses both first and second derivatives (gradient and Hessian)

This leads to more accurate approximations and faster convergence.

### Regularized Objective Function

The regularization term for each tree is defined as:

$$ \Omega(f) = \gamma T + \frac{1}{2}\lambda \sum_{j=1}^{T} w_j^2 $$

Where:
- $T$ is the number of leaf nodes in the tree
- $w_j$ is the score (weight) of leaf $j$
- $\gamma$ controls the penalty for adding more leaves (complexity)
- $\lambda$ is the L2 regularization parameter on leaf weights

**Intuition:**
- $\gamma T$: Penalizes trees with many leaves (encourages simpler trees)
- $\frac{1}{2}\lambda \sum_{j=1}^{T} w_j^2$: Penalizes large leaf weights (smooths predictions)

### Second-Order Approximation

For a given loss function $L$, XGBoost uses Taylor expansion up to the second order:

$$ L(y_i, \hat{y}_i^{(t-1)} + f_t(x_i)) \approx L(y_i, \hat{y}_i^{(t-1)}) + g_i f_t(x_i) + \frac{1}{2} h_i f_t^2(x_i) $$

Where:
- $g_i = \frac{\partial L(y_i, \hat{y}_i^{(t-1)})}{\partial \hat{y}_i^{(t-1)}}$ is the **first derivative (gradient)**
- $h_i = \frac{\partial^2 L(y_i, \hat{y}_i^{(t-1)})}{\partial (\hat{y}_i^{(t-1)})^2}$ is the **second derivative (Hessian)**

#### For Binary Classification (Log Loss):

$$ L(y, \hat{p}) = -[y\log(\hat{p}) + (1-y)\log(1-\hat{p})] $$

Where $\hat{p} = \sigma(F(x)) = \frac{1}{1 + e^{-F(x)}}$

**First derivative (gradient):**

$$ g_i = \frac{\partial L}{\partial F(x_i)} = \hat{p}_i - y_i $$

**Second derivative (Hessian):**

$$ h_i = \frac{\partial^2 L}{\partial F(x_i)^2} = \hat{p}_i(1 - \hat{p}_i) $$

**Note:** The gradient is the negative of the residual used in standard GBDT ($r_i = y_i - \hat{p}_i$)

### Tree Structure Score

After simplification (removing constant terms), the objective for tree $t$ becomes:

$$ \text{Obj}^{(t)} = \sum_{j=1}^{T} \left[ G_j w_j + \frac{1}{2}(H_j + \lambda)w_j^2 \right] + \gamma T $$

Where:
- $G_j = \sum_{i \in I_j} g_i$ is the sum of gradients for samples in leaf $j$
- $H_j = \sum_{i \in I_j} h_i$ is the sum of Hessians for samples in leaf $j$
- $I_j$ is the set of sample indices in leaf $j$

**Optimal weight for leaf $j$:**

By taking the derivative with respect to $w_j$ and setting it to zero:

$$ w_j^* = -\frac{G_j}{H_j + \lambda} $$

**Corresponding optimal objective (quality score):**

$$ \text{Obj}^* = -\frac{1}{2}\sum_{j=1}^{T} \frac{G_j^2}{H_j + \lambda} + \gamma T $$

This score tells us how "good" a particular tree structure is.

### Split Finding Algorithm

XGBoost evaluates splits by calculating the **gain** from splitting a leaf:

$$ \text{Gain} = \frac{1}{2}\left[ \frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - \frac{(G_L + G_R)^2}{H_L + H_R + \lambda} \right] - \gamma $$

Where:
- $G_L, H_L$ are the sum of gradients and Hessians for the **left** child
- $G_R, H_R$ are the sum of gradients and Hessians for the **right** child

**Decision rule:**
- If $\text{Gain} > 0$: The split improves the objective, so accept it
- If $\text{Gain} \leq 0$: The split doesn't help (or regularization penalty is too high), so reject it

**Algorithm:**
1. Start with all samples in one leaf
2. For each feature and each possible split point:
   - Calculate $G_L, H_L, G_R, H_R$
   - Calculate Gain
3. Choose the split with maximum positive gain
4. Recursively split child nodes until:
   - Gain becomes negative
   - Maximum depth is reached
   - Minimum samples in leaf is reached

### Python Implementation - From Scratch

```python
import numpy as np

def sigmoid(x):
    """Numerically stable sigmoid function."""
    return np.where(
        x >= 0,
        1 / (1 + np.exp(-x)),
        np.exp(x) / (1 + np.exp(x))
    )

class XGBoostTreeNode:
    """Node in an XGBoost regression tree."""
    def __init__(self):
        self.feature_idx = None
        self.threshold = None
        self.left = None
        self.right = None
        self.value = None  # leaf weight

class XGBoostTree:
    """Single tree in XGBoost with second-order optimization."""
    def __init__(self, max_depth=3, min_child_weight=1, reg_lambda=1.0, gamma=0.0): #gamma = 0 to make it simple.
        self.max_depth = max_depth
        self.min_child_weight = min_child_weight  # minimum sum of Hessian
        self.reg_lambda = reg_lambda
        self.gamma = gamma
        self.root = None

    def _calculate_leaf_weight(self, G, H):
        """Calculate optimal leaf weight."""
        return -G / (H + self.reg_lambda)

    def _calculate_gain(self, G_left, H_left, G_right, H_right, G_parent, H_parent):
        """Calculate the gain from a split."""
        gain = 0.5 * (
            (G_left ** 2) / (H_left + self.reg_lambda) +
            (G_right ** 2) / (H_right + self.reg_lambda) -
            (G_parent ** 2) / (H_parent + self.reg_lambda)
        ) - self.gamma
        return gain

    def _find_best_split(self, X, grad, hess):
        """Find the best split point for the data."""
        best_gain = -np.inf
        best_feature = None
        best_threshold = None

        G_parent = np.sum(grad)
        H_parent = np.sum(hess)

        n_samples, n_features = X.shape

        for feature_idx in range(n_features):
            # Sort by feature values
            sorted_indices = np.argsort(X[:, feature_idx])
            sorted_feature = X[sorted_indices, feature_idx]
            sorted_grad = grad[sorted_indices]
            sorted_hess = hess[sorted_indices]

            G_left = 0
            H_left = 0

            # Try each split point
            for i in range(n_samples - 1):
                G_left += sorted_grad[i]
                H_left += sorted_hess[i]
                G_right = G_parent - G_left
                H_right = H_parent - H_left

                # Skip if children don't meet minimum weight requirement
                if H_left < self.min_child_weight or H_right < self.min_child_weight:
                    continue

                # Skip if not a valid split point (same feature value)
                if sorted_feature[i] == sorted_feature[i + 1]:
                    continue

                gain = self._calculate_gain(G_left, H_left, G_right, H_right, G_parent, H_parent)

                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature_idx
                    best_threshold = (sorted_feature[i] + sorted_feature[i + 1]) / 2

        return best_feature, best_threshold, best_gain

    def _build_tree(self, X, grad, hess, depth=0):
        """Recursively build the tree."""
        node = XGBoostTreeNode()

        # Calculate leaf weight for current node
        G = np.sum(grad)
        H = np.sum(hess)

        # Stopping criteria
        if depth >= self.max_depth or len(X) < 2 or H < self.min_child_weight:
            node.value = self._calculate_leaf_weight(G, H)
            return node

        # Find best split
        best_feature, best_threshold, best_gain = self._find_best_split(X, grad, hess)

        # If no valid split found or gain is not positive
        if best_feature is None or best_gain <= 0:
            node.value = self._calculate_leaf_weight(G, H)
            return node

        # Split the data
        left_mask = X[:, best_feature] <= best_threshold
        right_mask = ~left_mask

        node.feature_idx = best_feature
        node.threshold = best_threshold

        # Recursively build left and right subtrees
        node.left = self._build_tree(X[left_mask], grad[left_mask], hess[left_mask], depth + 1)
        node.right = self._build_tree(X[right_mask], grad[right_mask], hess[right_mask], depth + 1)

        return node

    def fit(self, X, grad, hess):
        """Fit the tree to gradients and Hessians."""
        self.root = self._build_tree(X, grad, hess)

    def _predict_single(self, x, node):
        """Predict for a single sample."""
        if node.value is not None:
            return node.value

        if x[node.feature_idx] <= node.threshold:
            return self._predict_single(x, node.left)
        else:
            return self._predict_single(x, node.right)

    def predict(self, X):
        """Predict for all samples."""
        return np.array([self._predict_single(x, self.root) for x in X])

class XGBoostClassifier:
    """
    XGBoost binary classifier with second-order optimization.
    - Uses gradients and Hessians
    - Includes L2 regularization and complexity penalty
    """
    def __init__(self, n_estimators=50, learning_rate=0.1, max_depth=3,
                 min_child_weight=1, reg_lambda=1.0, gamma=0.0):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_child_weight = min_child_weight
        self.reg_lambda = reg_lambda
        self.gamma = gamma
        self.base_score_ = None
        self.trees_ = []

    def _init_score(self, y):
        """Initialize with log-odds."""
        p = np.clip(np.mean(y), 1e-6, 1 - 1e-6)
        return float(np.log(p / (1 - p)))

    def fit(self, X, y):
        """Fit the XGBoost classifier."""
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        assert set(np.unique(y)).issubset({0.0, 1.0}), "Labels must be 0/1."

        # Initialize base score
        self.base_score_ = self._init_score(y)
        F = np.full_like(y, self.base_score_, dtype=float)
        self.trees_ = []

        # Build trees sequentially
        for m in range(self.n_estimators):
            # Calculate probabilities
            p = sigmoid(F)

            # Calculate gradients and Hessians for log loss
            grad = p - y  # first derivative
            hess = p * (1 - p)  # second derivative

            # Fit tree to gradients and Hessians
            tree = XGBoostTree(
                max_depth=self.max_depth,
                min_child_weight=self.min_child_weight,
                reg_lambda=self.reg_lambda,
                gamma=self.gamma
            )
            tree.fit(X, grad, hess)

            # Update predictions
            update = tree.predict(X)
            F += self.learning_rate * update

            self.trees_.append(tree)

    def _decision_function(self, X):
        """Calculate raw scores (log-odds)."""
        X = np.asarray(X, dtype=float)
        F = np.full(X.shape[0], self.base_score_, dtype=float)
        for tree in self.trees_:
            F += self.learning_rate * tree.predict(X)
        return F

    def predict_proba(self, X):
        """Predict class probabilities."""
        F = self._decision_function(X)
        p = sigmoid(F)
        return np.vstack([1 - p, p]).T

    def predict(self, X):
        """Predict class labels."""
        proba = self.predict_proba(X)[:, 1]
        return (proba >= 0.5).astype(int)
```

### Python Implementation - Using XGBoost Library

#### Installation

```bash
pip install xgboost
```

#### Basic Classification Example

```python
import xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

# Create sample data
X, y = make_classification(n_samples=1000, n_features=20, n_informative=15,
                          n_redundant=5, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create XGBoost classifier
model = xgb.XGBClassifier(
    n_estimators=100,        # number of boosting rounds
    learning_rate=0.1,       # shrinkage rate (eta)
    max_depth=3,             # maximum tree depth
    min_child_weight=1,      # minimum sum of instance weight in a child
    gamma=0,                 # minimum loss reduction for split
    subsample=0.8,           # subsample ratio of training instances
    colsample_bytree=0.8,    # subsample ratio of columns when constructing each tree
    reg_alpha=0,             # L1 regularization term on weights
    reg_lambda=1,            # L2 regularization term on weights
    objective='binary:logistic',  # learning objective
    random_state=42
)

# Fit the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_proba)

print(f"Accuracy: {accuracy:.4f}")
print(f"AUC-ROC: {auc:.4f}")
```

#### Using DMatrix for Better Performance

```python
# Convert to DMatrix format (XGBoost's internal data structure)
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Set parameters
params = {
    'max_depth': 3,
    'eta': 0.1,  # learning rate
    'objective': 'binary:logistic',
    'eval_metric': 'auc',
    'lambda': 1,  # L2 regularization
    'alpha': 0,   # L1 regularization
    'gamma': 0    # minimum loss reduction
}

# Train with early stopping
evals = [(dtrain, 'train'), (dtest, 'test')]
bst = xgb.train(
    params,
    dtrain,
    num_boost_round=100,
    evals=evals,
    early_stopping_rounds=10,  # stop if no improvement for 10 rounds
    verbose_eval=10
)

# Make predictions
y_pred_proba = bst.predict(dtest)
y_pred = (y_pred_proba > 0.5).astype(int)
```

#### Cross-Validation

```python
# Perform cross-validation
cv_results = xgb.cv(
    params,
    dtrain,
    num_boost_round=100,
    nfold=5,
    metrics='auc',
    early_stopping_rounds=10,
    seed=42
)

print(f"Best AUC: {cv_results['test-auc-mean'].max():.4f}")
print(f"Best iteration: {cv_results['test-auc-mean'].idxmax() + 1}")
```

#### Feature Importance

```python
import matplotlib.pyplot as plt

# Get feature importance
importance = model.feature_importances_
feature_names = [f'feature_{i}' for i in range(X.shape[1])]

# Plot
plt.figure(figsize=(10, 6))
plt.barh(feature_names, importance)
plt.xlabel('Feature Importance')
plt.title('XGBoost Feature Importance')
plt.tight_layout()
plt.show()

# Or use XGBoost's built-in plotting
xgb.plot_importance(model, max_num_features=10)
plt.show()
```

### Key Hyperparameters Summary

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `n_estimators` | Number of boosting rounds (trees) | 50-1000 |
| `learning_rate` (eta) | Step size shrinkage to prevent overfitting | 0.01-0.3 |
| `max_depth` | Maximum tree depth | 3-10 |
| `min_child_weight` | Minimum sum of Hessian in a child | 1-10 |
| `gamma` | Minimum loss reduction for split | 0-5 |
| `subsample` | Fraction of samples used per tree | 0.5-1.0 |
| `colsample_bytree` | Fraction of features used per tree | 0.5-1.0 |
| `reg_lambda` | L2 regularization | 0-10 |
| `reg_alpha` | L1 regularization | 0-10 |

### Tips for Tuning XGBoost

1. **Start with default parameters** and establish a baseline
2. **Tune tree-specific parameters first**: `max_depth`, `min_child_weight`
3. **Add regularization**: `gamma`, `reg_lambda`, `reg_alpha`
4. **Add randomness**: `subsample`, `colsample_bytree`
5. **Lower learning_rate** and increase `n_estimators` for final model
6. **Use early stopping** to prevent overfitting
7. **Cross-validation** is essential for hyperparameter tuning
