import numpy as np


def roll(sides: int = 6) -> int:
    return np.random.randint(1, sides + 1)


def rolln(n: int, sides: int = 6) -> np.ndarray:
    return np.random.randint(1, sides + 1, n)


def reroll_1s(rolls: np.ndarray) -> np.ndarray:
    reroll_mask = (rolls == 1)
    rolls[reroll_mask] = np.random.randint(1, rolls.max() + 1, reroll_mask.sum())
    return rolls
