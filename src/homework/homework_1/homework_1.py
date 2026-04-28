import pandas as pd
import numpy as np
import torch 
from typing import Literal, Callable

#labels = [1,1,0,0,1,1,1,0,0,1] # example list of class labels. total = 10 --> 4 0's, 6 1's.

#def entropy_numpy(labels): # defining a function, calling that function entropy_numpy, and this function takes ONE input which I am calling "labels"; g(x) = y <--> entropy_numpy(labels) = y. 
""" 

Calculate entropy using Numpy. 
    
Formula: H(S) = -Σ(p_i × log₂(p_i))
    
Args: labels: numpy array of class labels
    
Returns: entropy value (float)

""" 

# Step 1: Count occurrences of each unique class. 
#_, counts = np.unique(labels, return_counts=True) # np.unique finds all unique values/elements in array and return_counts gives you the number of times each unique value appears in the array. so it will return back two values: 1) unique values, and 2) counts of those unique values. 
# counts = --> var name where we store information. It's an array --< array = list of items stored in order.  
''' Regular Python list:
my_list = [10, 20, 30, 40]

Position:   0   1   2   3
Value:     10  20  30  40
''' 
#_, counts = counts 
#counts, _ = counts
#print(counts)
#print(_, counts)

# Step 2: Calculate probabilities for each class. Division automatically broadcasta across all counts. 
#probabilities = counts / len(labels) # len(labels) = total number of labels = 10.

# Step 3: Handle log(0) issue - filter out zero probabilities. b/c log(0) is undefined. 
#probabilities = probabilities[probabilities > 0]. # boolean indexing to filter out zero probabilities. keep only values > 0. 

# Step 4: Calculate entropy 
#entropy = -np.sum(probabilities * np.log2(probabilities). # element-wise multiplication of probabilities with log2(probabilities), then sum all those values using np.sum, and multiply by -1 to get final entropy value. this is the equation/formula for entropy. 
                      
#return entropy
                      




## Entropy 

test_labels = np.array([1,1,0,1,0,0,0])

def entropy_numpy(test_labels: np.ndarray, log_choice: Literal['log2', 'log10'] = 'log2') -> np.floating:

    """
    ## Docstring for entropy_numpy
    
    ### Description

    - This is a numpy-based implementation of entropy.

    ### Input Parameters
    - test_labels (np.ndarray) : Labels to use for computing entropy from the set.

    ### Output
    - entropy (np.floating) : Floating point result after computing the entropy score.
    """

    log_choice_dict = {
        'log2' : np.log2,
        'log10' : np.log10
    }

    _, counts = np.unique(test_labels, return_counts=True)
    probabilities = counts / len(test_labels)

    log_func: Callable = log_choice_dict[log_choice]
    print(type(log_func))
    
    # Calculating the log probabilities
    log_proba = log_func(probabilities)
    print(log_proba)

    entropy = -np.sum(probabilities * log_proba)

    return entropy

print(f"Entropy: {entropy_numpy(test_labels)}")
print(entropy_numpy(test_labels)*100)



## Gini Impurity

test_labels_2 = np.array([1,1,0,1,0,0,0])

def gini_numpy(test_labels_2): 
    _, counts = np.unique(test_labels_2, return_counts=True)
    probabilities = counts / len(test_labels_2)
    squared_prob = probabilities ** 2 
    gini = 1 - np.sum(squared_prob)
    return gini 

print(f"Gini Impurity: {gini_numpy(test_labels_2)}") 
print(gini_numpy(test_labels_2)*100)

