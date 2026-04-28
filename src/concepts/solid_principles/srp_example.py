from typing import List

# Function that is trying to add 2 numbers together
def add(x: int, y: int) -> int:
    return x + y

# Dot Product - Non SRP Way
def dot(x: List[int], y: List[int]) -> int:

    # Result and initialize to 0
    result = 0

    if len(x) == len(y):
        # Multiply the numbers at the same index
        for i in range(len(x)):
            # Value for x
            value_x = x[i]

            # Value for y
            value_y = y[i]

            # Update the result by multipling 2 values
            result += value_x * value_y
    
    else:
        print("The lists are not the same length so the dot product cannot be calculated.")
    
    return result

# Dot Product

## 1. Initialize the result with a value
## 2. Multiply numbers at the same index
## 3. Update the initialized value with the multiplied numbers

def initialize_value(x: int) -> int:
    return x

def multiply_at_same_idx(x: list[int], y: list[int], i: int) -> int:
    # Values
    value_x = x[i]
    value_y = y[i]
    return value_x * value_y

def update_value(initial_value: int, value_to_update: int) -> int:
    return initial_value + value_to_update

def dot(x: list[int], y: list[int]) -> int:

    result = initialize_value(x=0)

    for i in range(len(x)):
        value = multiply_at_same_idx(x=x, y=y, i=i)

        result = update_value(initial_value=result, value_to_update=value)
    
    return result