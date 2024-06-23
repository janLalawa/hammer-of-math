import numpy as np
from numpy import bool_

from utils.dice import roll


def wound_roll_needed(strength, toughness) -> int:
    if strength >= 2 * toughness:
        return 2
    elif strength > toughness:
        return 3
    elif strength == toughness:
        return 4
    elif strength > 0.5 * toughness:
        return 5
    else:
        return 6


def save_roll_needed(ap, save, invuln=None) -> int:
    modified_save = save - ap
    if invuln is None:
        return max(2, min(6, modified_save))
    else:
        return max(2, min(6, min(modified_save, invuln)))


def calculate_fnp_damage(
        wounds: int, damage_per: int, fnp_threshold: int
) -> tuple[int, int]:
    total_damage = wounds * damage_per
    for _ in range(total_damage):
        dice_roll = roll()
        if dice_roll >= fnp_threshold:
            total_damage -= 1
    wounds_taken = total_damage // damage_per
    fractional_wound = total_damage % damage_per
    return wounds_taken, fractional_wound


def count_success(rolls: np.ndarray, threshold: int, modifier: int = 0) -> bool_:
    if modifier != 0:
        return np.sum(rolls + modifier >= threshold)
    return np.sum(rolls >= threshold)


def count_equal_value_in_list(rolls: np.ndarray, value: int) -> int:
    return np.sum(rolls == value)


def dice_check(r: int, threshold: int, modifier: int = 0) -> bool:
    if modifier != 0:
        return r + modifier >= threshold
    return r >= threshold


def calc_percentage(n, total) -> float:
    return (n / total) * 100
