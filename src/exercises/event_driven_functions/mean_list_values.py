from functools import reduce

"""

Event Driven Functions Exercise

- Imagine you have a list which contains a bunch of lists inside of it.

    - Get the sum of all the numbers in each list.
    - Take the average of those numbers and get an output.

    - Don't use loops.
    - Only use event-driven functions
        - reduce
        - filter
        - map

"""

"""

Solution with sum()

"""

# List of Lists
list_of_lists = [[i*j for i in range(100)] for j in range(1, 11)]

print(list_of_lists)

# Sum up the numbers in each list
result = map(lambda x: sum(x), list_of_lists)

print(result)

# List
result = list(result)

# Sum
avg = sum(result) / len(result)

print(avg)

"""

Solution with functools.reduce()

"""

# Reduce
result = list(map(lambda s: reduce(lambda a,b: a+b, s), list_of_lists))

print(result)

avg = reduce(lambda a,b: a+b, result) / len(result)

print(avg)