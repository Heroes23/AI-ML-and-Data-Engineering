## Random Forests

### Description

- A random forest is an ensemble algorithm that trains multiple decision trees in parallel where each decision tree is essentially learning patterns from different, random subsets of the original sample of data.

### Mechanism

- Each decision tree is having its own information gain optimization.
- Each tree sees a random subset of the original set of features.
- Once you get a prediction from each tree, you want to cast a majority vote across the trees.

#### Mathematical Intuition

- Training Dataset

$$ D = \{(x_i , y_i)\}_{i=1}^{N} $$

- Parameter: `n_estimators`
    - The individual tree can be represented as `b`.
    - Create a random sample of size `N` with replacement from the original training set `D`.

- Predictions from a decision tree can be represented as $h_b(x)$.

- Majority Vote

$$ \hat{y}(x) = \argmax_{k} \frac{1}{B} \sum_{b=1}^{B} 1\{h_b(x) = k \} $$