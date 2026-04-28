from math import log2
from collections import Counter

def gini_v1(labels: list[str]) -> float:

    """
    Description: Calculating the Gini impurity for a list of values.
    
    """

    # Gini Impurity result
    result_sum = 0

    # Get the proportions for the labels
    label_set = list(set(labels))

    # Iterate through our unique labels
    for label in label_set:

        # Get the frequency of the label
        freq = labels.count(label)

        # Proportion
        p = freq / len(labels)

        # Square the proportion
        impurity = p ** 2

        # Adding the products together
        result_sum = result_sum + impurity
    
    return 1 - result_sum


def gini_v2(labels: list[str]) -> float:

    # Result for Gini impurity
    result_sum = 0

    # Counter
    counter = Counter(labels)

    # Get the label and associated count
    for count in counter.values():

        # Get the proportion
        p = count / len(labels)

        # Square the proportion
        impurity = p ** 2

        # Adding the impurities together
        result_sum = result_sum + impurity
    
    return 1 - result_sum



# Sample labels
samples = ['A', 'A', 'B', 'B', 'B', 'A']

sample_counter = Counter(samples)

print(sample_counter)

# Gini v1
gini_v1_result = gini_v1(labels=samples)

print(gini_v1_result)

gini_v2_result = gini_v2(labels=samples)

print(gini_v2_result)