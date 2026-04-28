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