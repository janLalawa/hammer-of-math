from config.constants import GameSettings
from core.traits import *
from core.units import *
from utils.calculations import (
    save_roll_needed,
    count_success,
    count_equal_value_in_list,
)
from utils.dice import rolln


def sim_saves(wounds: Rolls, attacking_unit: Unit, defender: Unit) -> Rolls:
    saves = Rolls(wounds.successes, rolln(wounds.successes))
    saves.attempts = wounds.successes

    save_threshold = save_roll_needed(
        (attacking_unit.weapon.ap + GameSettings.EXTRA_AP), defender.save, defender.invuln
    )

    saves.successes = count_success(saves.rolls, save_threshold)
    saves.failures = saves.attempts - saves.successes
    saves.ones = count_equal_value_in_list(saves.rolls, 1)
    saves.crits = count_equal_value_in_list(saves.rolls, GameSettings.CRIT)
    saves.final_rolls = saves.rolls
    return saves
