import numpy as np
from core.rolls import Rolls

from core.units import *


def sim_wound_damage_list(fnp: Rolls, attacking_unit: Unit) -> np.ndarray:
    wounds_taken = fnp.failures // attacking_unit.weapon.damage
    fractional_wound = fnp.failures % attacking_unit.weapon.damage
    wound_damage_list = np.full(wounds_taken, attacking_unit.weapon.damage)
    if fractional_wound > 0:
        wound_damage_list = np.append(wound_damage_list, fractional_wound)
    return wound_damage_list


def sim_models_killed(wound_damage_list: np.ndarray, defender: Unit, defender_model_wounds: np.ndarray):
    models_killed, defender_remaining_wounds = calculate_models_killed(defender_model_wounds, wound_damage_list)
    return models_killed, defender_remaining_wounds


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
