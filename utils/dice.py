import numpy as np


def roll(sides: int = 6) -> int:
    return np.random.randint(1, sides + 1)


def rolln(n: int, sides: int = 6) -> np.ndarray:
    return np.random.randint(1, sides + 1, n)


def reroll_1s(rolls: np.ndarray) -> np.ndarray:
    reroll_mask = (rolls == 1)
    rolls[reroll_mask] = np.random.randint(1, rolls.max() + 1, reroll_mask.sum())
    return rolls


def roll_parsed_dice(dice: str) -> np.ndarray:
    if not dice:
        return np.array([])

    if "d" in dice:
        n, sides = dice.split("d")
        n = int(n) if n else 1
        return rolln(int(n), int(sides))

    return np.array([int(dice)])
