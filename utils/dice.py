import random

import numpy as np


def roll(sides: int = 6):
    return np.random.randint(1, sides + 1)


def rolln(n: int, sides: int = 6) -> np.ndarray:
    """
    Rolls a die n times and returns an array of the results.
    :param n: The number of times to roll the die.
    :param sides: The count of sides on the die. (Default 6)
    :return: An array of the results of the die rolls.
    """
    return np.random.randint(1, sides + 1, n)


def reroll_1s(rolls: np.ndarray) -> np.ndarray:
    reroll_mask = (rolls == 1)
    rolls[reroll_mask] = np.random.randint(1, rolls.max() + 1, reroll_mask.sum())
    return rolls
