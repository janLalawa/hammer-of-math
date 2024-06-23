from config.constants import GameSettings
from core.traits import *
from core.units import *
from utils.calculations import (
    wound_roll_needed,
    count_success,
    count_equal_value_in_list,
)
from utils.dice import rolln


def sim_wounds(hits: Rolls, attacking_unit: Unit, defender: Unit) -> Rolls:
    wounds = Rolls(hits.successes, rolln(hits.successes))
    wounds.attempts = hits.successes

    wound_threshold = wound_roll_needed(
        attacking_unit.weapon.strength, defender.toughness
    )

    wounds.successes = count_success(wounds.rolls, wound_threshold)
    wounds.failures = wounds.attempts - wounds.successes
    wounds.ones = count_equal_value_in_list(wounds.rolls, 1)
    wounds.crits = count_success(wounds.rolls, GameSettings.CRIT)

    if lethal_hits in attacking_unit.traits or lethal_hits in attacking_unit.weapon.traits:
        wounds.successes += hits.crits

    wounds.final_rolls = wounds.rolls
    return wounds
