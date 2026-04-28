## Entropy

### Description

- Entropy measures the uncertainty or impurity of a specific node that might appear in a structure like a tree.

- In the context of decision trees, if all the samples of your data happen to be in one class, the entropy would be considered as pure or `0`.

    - If it's evenly distributed, entropy would be maximum which implies it would be `1`.

### Calculation

$$ H(S) = - \sum_{j=1}^{K} p_j \log_2(p_j) $$

- `j` refers to the index associated with a data point in your sample of data.

- `K` which is the total number of points in your data sample.

- $p_j$ is the proportion of that particular value at the index (frequency)

#### Example

- Assume that you have some characters in a sequence below.

### $$ [A, A, B, B, B, A] $$

1. Find the proportions associated with each character.

$$ p(A) = \frac{3}{6} = 0.5 $$
$$ p(B) = \frac{3}{6} = 0.5 $$

2. Multiply the proportions with the $ \log_2 $ transform on the same proportion.

$$ p(A) \log_2 p(A) = 0.5 * \log_2 (0.5) $$

$$ p(B) \log_2 p(B) = 0.5 * \log_2 (0.5) $$

3. Add the products together.

$$ H(S) = (0.5 * \log_2 (0.5)) + (0.5 * \log_2 (0.5)) $$

### Python Example

```python
from math import log2
from collections import Counter

def entropy_v1(labels: list[str]) -> float:

    """
    Description: Calculating the entropy for a list of values.
    
    """

    # Entropy
    result_entropy = 0

    # Get the proportions for the labels
    label_set = list(set(labels))

    # Iterate through our unique labels
    for label in label_set:

        # Get the frequency of the label
        freq = labels.count(label)

        # Proportion
        p = freq / len(labels)

        # Product with the log transform
        ent = p * log2(p)

        # Adding the products together
        result_entropy = result_entropy + ent
    
    return -1 * result_entropy


def entropy_v2(labels: list[str]) -> float:

    # Result for entropy
    result_entropy = 0

    # Counter
    counter = Counter(labels)

    # Get the label and associated count
    for count in counter.values():

        # Get the proportion
        p = count / len(labels)

        # Product with the log transform
        ent = p * log2(p)

        # Adding the products together
        result_entropy = result_entropy + ent
    
    return -1 * result_entropy



# Sample labels
samples = ['A', 'A', 'B', 'B', 'B', 'A']

sample_counter = Counter(samples)

print(sample_counter)

# Entropy v1
entropy_v1_result = entropy_v1(labels=samples)

print(entropy_v1_result)

entropy_v2_result = entropy_v2(labels=samples)

print(entropy_v2_result)
```