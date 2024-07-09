import numpy as np

from config.constants import GameSettings
from core import Scenario
from core.rolls import Rolls
from core.units import *
from utils.dice import rolln


def sim_fnp_scenario(scenario: Scenario, atk_model_group: ModelGroup, wep_idx: int = 0) -> Rolls:
    fnp = scenario.rolls_fnp
    total_damage = scenario.rolls_saves.failures * atk_model_group.model.weapons[wep_idx].damage
    fnp.rolls = rolln(total_damage)

    fnp_threshold = scenario.defender.model.fnp
    fnp.successes = np.sum(fnp.rolls >= fnp_threshold)
    fnp.failures = total_damage - fnp.successes
    fnp.ones = np.sum(fnp.rolls == 1)
    fnp.crits = np.sum(fnp.rolls >= GameSettings.CRIT)
    fnp.final_rolls = fnp.rolls

    return fnp
