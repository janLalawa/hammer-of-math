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


def calculate_models_killed(defender_model_wounds, wound_damage_list):
    models_killed = 0
    current_model_index = 0
    total_models = len(defender_model_wounds)

    for damage in wound_damage_list:
        if current_model_index >= total_models:
            break

        current_model_wounds = defender_model_wounds[current_model_index]

        if damage >= current_model_wounds:
            # Kill the model and move to the next
            defender_model_wounds[current_model_index] = 0
            models_killed += 1
            current_model_index += 1
        else:
            # Damage the current model
            defender_model_wounds[current_model_index] -= damage

    return models_killed, defender_model_wounds


def count_success(rolls: list[int], threshold: int, modifier: int = 0) -> int:
    success_count = 0
    for r in rolls:
        if dice_check(r, threshold, modifier):
            success_count += 1
    return success_count


def count_equal_value_in_list(rolls: list[int], value: int) -> int:
    return sum(1 for r in rolls if r == value)


def dice_check(r: int, threshold: int, modifier: int = 0) -> bool:
    if modifier != 0:
        return r + modifier >= threshold
    return r >= threshold


def calc_percentage(n, total) -> float:
    return (n / total) * 100
