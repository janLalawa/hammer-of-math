import numpy as np

from config.constants import GameSettings
from core import Scenario
from core.rolls import Rolls
from core.units import *
from utils.calculations import save_roll_needed
from utils.dice import rolln


def sim_saves_scenario(scenario: Scenario, atk_model_group: ModelGroup) -> Rolls:
    saves = scenario.rolls_saves

    saves.attempts = scenario.rolls_wounds.successes
    saves.rolls = rolln(scenario.rolls_saves.attempts)

    save_threshold = save_roll_needed(
        atk_model_group.model.weapon.ap + GameSettings.EXTRA_AP,
        scenario.defender.model.save,
        scenario.defender.model.invuln,
    )

    saves.successes = np.sum(saves.rolls >= save_threshold)
    saves.failures = saves.attempts - scenario.rolls_saves.successes
    saves.ones = np.sum(saves == 1)
    saves.crits = np.sum(saves.rolls >= GameSettings.CRIT)
    saves.final_rolls = saves

    return saves
