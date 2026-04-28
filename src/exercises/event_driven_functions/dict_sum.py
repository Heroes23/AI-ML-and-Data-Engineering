from functools import reduce

customers = {
    'customer_one': list(range(1, 11)),
    'customer_two' : list(range(11, 21)),
    'customer_three' : list(range(21, 31))
}

# Creating your own function
def update_dict(a: dict, b: dict) -> dict:

    b.update(a)

    return b


# Event Driven Manner
result = map(lambda s: {s[0] : reduce(lambda a,b: a+b, s[1])}, customers.items())
result = reduce(lambda a,b: update_dict(a,b), list(result), {})

print(result)


