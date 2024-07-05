import numpy as np

from config.constants import GameSettings
from core.rolls import Rolls
from core.units import *
from utils.calculations import wound_roll_needed

from utils.dice import rolln


def sim_wounds(hits: Rolls, attacking_unit: Unit, defender: Unit) -> Rolls:
    wounds = Rolls(hits.successes, rolln(hits.successes))
    wounds.attempts = hits.successes

    wound_threshold = wound_roll_needed(attacking_unit.weapon.strength, defender.toughness)
    wounds.successes = np.sum(wounds.rolls >= wound_threshold)
    wounds.failures = wounds.attempts - wounds.successes
    wounds.ones = np.sum(wounds.rolls == 1)
    wounds.crits = np.sum(wounds.rolls >= GameSettings.CRIT)

    for ability in attacking_unit.abilities:
        if ability.name == "Lethal Hits":
            wounds = ability.apply_special(hits, wounds)

    wounds.final_rolls = wounds.rolls
    return wounds
