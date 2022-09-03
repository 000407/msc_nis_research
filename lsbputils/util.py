import random


def get_random_secret(length: int):
    return random.randrange(
        2 ** (length - 1),
        2 ** length
    )
