from functools import reduce

# Quickest way to get the numbers 1 through 10; 
nums = list(range(1, 11)) #make it 11 for 1-10. convert range to list. 


print(nums)

# Variable to store the result; 
result = 1

# Iterate through the numbers; 
for num in nums: #for loop 

    # Square the num; 
    sq_num = num * num

    # Update the result; 
    result = result * sq_num

print(result)

# Event driven functions

"""
1. map()
2. reduce()
3. filter()

"""
### Done without a 'for' loop: 

## map()
## Product
result = reduce(lambda a,b: a*b, map(lambda x: x**2, nums))

print(f"Product: {result}")

## Sum
result = reduce(lambda a,b: a+b, map(lambda x: x**2, nums))

print(f"Sum: {result}")