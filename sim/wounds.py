import numpy as np

from config.constants import GameSettings
from core import Scenario
from core.rolls import Rolls
from core.units import *
from utils.calculations import wound_roll_needed

from utils.dice import rolln


def sim_wounds_scenario(scenario: Scenario, atk_model_group: ModelGroup, wep_idx: int = 0) -> Rolls:
    wounds = scenario.rolls_wounds
    wounds.attempts = scenario.rolls_hits.successes
    wounds.rolls = rolln(wounds.attempts)

    wound_threshold = wound_roll_needed(
        atk_model_group.model.weapons[wep_idx].strength, scenario.defender.model.toughness
    )
    wounds.successes = np.sum(wounds.rolls >= wound_threshold)
    wounds.failures = wounds.attempts - wounds.successes
    wounds.ones = np.sum(wounds.rolls == 1)
    wounds.crits = np.sum(wounds.rolls >= GameSettings.CRIT)

    for ability in atk_model_group.model.abilities:
        if ability.name == "Lethal Hits":
            wounds = ability.apply_special(scenario.rolls_hits, wounds)

    wounds.final_rolls = wounds.rolls
    return wounds
