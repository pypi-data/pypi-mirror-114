def is_even(n):
    return n % 2 == 0


def is_odd(n):
    return not is_even(n)


import random as rnd


def get_lottery_numbers(min_value, max_value, size):
    numbers = set([])
    while len(numbers) < size:
        numbers.add(rnd.randint(min_value, max_value))
    numbers = list(numbers)
    numbers.sort()
    return numbers


lost_numbers = (4, 8, 15, 16, 23, 42)
