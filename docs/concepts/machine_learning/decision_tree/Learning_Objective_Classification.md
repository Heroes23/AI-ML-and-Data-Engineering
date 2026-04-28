## Decision Tree - Learning for Classification

### Description

- A decision tree repeatedly splits data into smaller groups that have more information gain (more purity).

### Mechanism

1. Pass in all the features to your decision tree.

2. Create various splits of data from your features and we then aim to evaluate each split.

3. Use a criterion (e.g. entropy, gini impurity) and compute information gain to see if the split is good quality.

- Stopping Criteria
    - Maximum depth within a tree
    - Minimum number of samples for each split
    - A particular node cannot be any more pure
- Threshold
    - As soon as the information gain hits `x`, then the learning basically stops.

- Classification Interpretation
    - If you have reached the optimal information gain for a node, then the node is representative of one class.

### Optimization

- Choose a criterion
    - Entropy
    - Gini impurity

#### Information Gain for Each Split

$$ \text{Left Gain} = \text{Impurity(\text{Parent})} - \text{Impurity(\text{Left Node})} $$

$$ \text{Right Gain} = \text{Impurity(\text{Parent})} - \text{Impurity(\text{Right Node})} $$



