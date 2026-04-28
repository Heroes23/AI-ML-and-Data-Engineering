## Gradient Boosted Decision Trees

### Topics

1. Tree Learning as Optimization
2. Log Loss
3. New Prediction Function
4. Constant Log-Odds
5. Negative Gradient Calculation
6. Python Implementation - Classifier - From Scratch
7. Python Implementation - Classifier - scikit-learn

### Tree Learning as Optimization

- For a normal decision tree, you split the features to best separate the target classes using strategies such as information gain until you reach some stopping point (e.g. max depth, minimum samples in a leaf node)

- In gradient boosting, we interpret learning in the sense where instead of trying to trust our predictions solely on one decision tree, we are actually building many trees.
    - The trees are following a sequence where the next tree aims to reduce the mistakes (e.g. residuals) from the prior tree.
        - This is accomplished by aiming to minimize a loss function which for classification problems is called log-loss.
        - Ultimately, the final tree that minimizes the loss should be the one that is used for making predictions.

### Log Loss

- Assume you have two classification labels or classes (0, 1).

$$ y \in \{0, 1\} $$

- $\hat{p}$ is the probability of a prediction being one of the two binary outcomes.

- Calculating the probability
    - Use the `softmax` function ($\sigma$)

$$ \sigma(x) = \frac{1}{1 + e^{-x}} $$

- We can define log loss as a function of $y$ and $\hat{p}$ .

$$ L(y, \hat{p}) = - [y\log{\hat{p}} + (1-y)\log{(1-\hat{p})}] $$

$$ \hat{p}(F(x)) = \frac{1}{1 + e^{-F(x)}} $$

- $F(x)$ refers to the function that is learned from the gradient boosted decision tree to get the score needed to retrieve a probability value after going through the sigmoid operation.

### New Prediction Function

$$ F_M(x) = F_0(x) + \sum_{m=1}^{M}v \cdot f_m(x) $$

- $f_m(x)$ refers to the scores retrieved from new decision trees being developed to optimize on the prior decision tree.

- $v$ refers to a learning rate (hyperparameter)

- $F_0(x) $ refers to the constant log-odds (score) which acts as an initial prediction associated with prior beliefs about what the prediction could be.

### Constant Log Odds

- We first want to get the proportion of positive class values in the training set:

$$ \overline{p} = \frac{1}{N} \sum_{i=1}^{N}y_i $$

- The constant log odds is then defined as:

$$ F_0(x) = \log(\frac{\overline{p}}{1 - \overline{p}}) $$

#### Worked Out Example

- For labels 0 and 1, let's say you have 100 training samples and 30 points that have a label of 1.

$$ \overline{p} = \frac{30}{100} = 0.3 $$

$$ F_0 = \log{(\frac{\overline{p}}{1 - \overline{p}})} = \log{\frac{0.3}{0.7}} \approx -0.847 $$

### Negative Gradient Calculation

- We want to see how far off the prediction is from the actual label.
    - To do this, we can define the negative gradient as a residual (probability difference from the label of the data point)

$$ r_i = y_i - \hat{p_i} $$

- If $r_i$ is positive, the probability is underestimating.

- If $r_i$ is negative, the probability is overestimating.

#### Goal and Intuition

- We then treat the residuals as continuous targets to predict as part of a regression problem

- The regression tree ends up splitting features to separate out the residuals obtained for the 1 and 0 labels from the training set

- The score obtained from the regression tree gets added to the initial constant log-odds to produce different scores for each sample with the intent that a combined prediction will now reduce the residual in future iterations.

#### Worked Out Example

- Use the same $F_0$ as above.
- Let's use $v = 0.01 $ as a learning rate.
- Let's say $f_1(x)$ gives you a score of 0.6

- Gradient Boosting Formula

$$ F_1{(x)} = F_0{(x)} + vf_1(x) $$

- First, let's get the probability of $F_0(x)$.

$$ \hat{p}(F_0(x)) = \frac{1}{1 + e^{-F_0(x)}} \rightarrow \frac{1}{1 + e^{-0.847}} \approx 0.3 $$

- Now we want to calculate the negative gradient from the predictions.

- For one sample, let's say the expected label should be 1.

$$ r_1 = 1 - 0.3 = 0.7 $$

- Assuming you do the above for samples in training set, you'll end up getting 0.7 for any data points with label being 1 and -0.3 for any points with label of 0.

- Now let's say a regression tree is trained to find the best feature splits to easily predict the 0.7 or -0.3 continuous values.

- After getting the function from the tree, we now get a score from the prediction. Let's say it happens to be `0.6`.

Now, our updated score will be:

$$ F_1(x) = -0.847 + 0.01(0.6) = -0.841  $$

- We can now get the probability of this score:

$$ \hat{p}(F_1(x)) = \frac{1}{1 + e^{0.841}} \approx 0.3013 $$

- Now calculate the new residuals


```math
\begin{aligned}

r_i^{(m)} = \begin{cases}

1 - p_i^{(m-1)} & y = 1 \\
0 - p_i^{(m-1)} & y = 0

\end{cases}

\end{aligned}
```

- Fit a new regression tree to capture feature splits that can lead to predicting the above residuals for all the samples in the training set.

- Get the new score and add to the existing $F_m(x)$ score.

- Continue this process iteratively until you reach the total number of iterations you set up as part of the gradient boosting.

### Python Implementation - From Scratch

```python
import numpy as np

# Import the Regression Tree
from regression_tree import RegressionTree

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
```

### Scikit-Learn Implementation

1. Install scikit-learn.

```bash
pip install scikit-learn
```

2. Import the `GradientBoostingClassifier`

```python
from sklearn.ensemble import GradientBoostingClassifier

gb = GradientBoostingClassifier(
    loss='log_loss',
    learning_rate=0.1,
    n_estimators=100,
    max_depth=3,
    random_state=42
)
```

3. Fit on your data

```python
...

X_train, y_train = ...

gb.fit(X_train,y_train)
```

4. Make predictions

```python
...

y_pred = gb.predict(X_test)
```

