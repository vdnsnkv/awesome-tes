from random import randint


def select_random_element(iterable):
    random_ix = randint(0, len(iterable) - 1)
    return iterable[random_ix]
