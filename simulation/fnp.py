from config.constants import GameSettings
from core.traits import *
from core.units import *
from utils.calculations import (
    count_success,
    count_equal_value_in_list,
)
from utils.dice import rolln


def sim_fnp(saves: Rolls, attacking_unit: Unit, defender: Unit) -> Rolls:
    total_damage = saves.failures * attacking_unit.weapon.damage

    fnp = Rolls(total_damage, rolln(total_damage))

    fnp.successes = count_success(fnp.rolls, defender.fnp)
    fnp.failures = fnp.attempts - fnp.successes
    fnp.ones = count_equal_value_in_list(fnp.rolls, 1)
    fnp.crits = count_equal_value_in_list(fnp.rolls, GameSettings.CRIT)
    fnp.final_rolls = fnp.rolls
    return fnp
