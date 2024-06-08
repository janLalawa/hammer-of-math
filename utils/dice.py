import random


def roll(sides: int = 6):
    return random.randint(1, sides)


def rollx(n: int, sides: int = 6) -> list[int]:
    """
    Rolls a die n times and returns a list of the results.
    :param n: The number of times to roll the die.
    :param sides: The count of sides on the die. (Default 6)
    :return: A list of the results of the die rolls.
    """
    return [roll(sides) for _ in range(n)]


def reroll_1s(rolls: list[int]) -> list[int]:
    return [roll() if r == 1 else r for r in rolls]
