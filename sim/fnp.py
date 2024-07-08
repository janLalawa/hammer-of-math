import numpy as np

from config.constants import GameSettings
from core import Scenario
from core.rolls import Rolls
from core.units import *
from utils.dice import rolln


def sim_fnp_scenario(scenario: Scenario) -> Rolls:
    saves = scenario.rolls_saves
    attacker = scenario.attackers[0][0]
    defender = scenario.defender[0]
    return sim_fnp(saves, attacker, defender)


def sim_fnp(saves: Rolls, attacking_unit: Unit, defender: Unit) -> Rolls:
    total_damage = saves.failures * attacking_unit.weapon.damage
    fnp = Rolls(total_damage, rolln(total_damage))

    fnp_threshold = defender.fnp
    fnp.successes = np.sum(fnp.rolls >= fnp_threshold)
    fnp.failures = fnp.attempts - fnp.successes
    fnp.ones = np.sum(fnp.rolls == 1)
    fnp.crits = np.sum(fnp.rolls >= GameSettings.CRIT)
    fnp.final_rolls = fnp.rolls
    return fnp
