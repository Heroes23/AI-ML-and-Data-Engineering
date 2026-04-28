from functools import reduce

"""

Sum of Even Numbers

"""

# For Loops
nums = list(range(1, 11))

count = 0

for num in nums:

    # Check if the number is even
    if num % 2 == 0:

        # Add the number to the count
        count += num

print(count)

"""

Event Driven Functions

"""

result = reduce(lambda a,b: a+b, filter(lambda x: x % 2 == 0, nums))

print(result)