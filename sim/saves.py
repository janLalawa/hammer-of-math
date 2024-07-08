import numpy as np

from config.constants import GameSettings
from core.rolls import Rolls
from core.units import *
from utils.calculations import save_roll_needed
from utils.dice import rolln


def sim_saves(wounds: Rolls, attacking_unit: Unit, defender: Unit) -> Rolls:
    saves = Rolls(wounds.successes, rolln(wounds.successes))
    saves.attempts = wounds.successes

    save_threshold = save_roll_needed(
        attacking_unit.weapon.ap + GameSettings.EXTRA_AP, defender.save, defender.invuln
    )
    saves.successes = np.sum(saves.rolls >= save_threshold)
    saves.failures = saves.attempts - saves.successes
    saves.ones = np.sum(saves.rolls == 1)
    saves.crits = np.sum(saves.rolls >= GameSettings.CRIT)
    saves.final_rolls = saves.rolls
    return saves
