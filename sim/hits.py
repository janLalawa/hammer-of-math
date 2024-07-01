import numpy as np

from config.constants import GameSettings
from core.traits_DEPRECATED import *
from core.units import *
from utils.dice import rolln


def sim_hits(unit: Unit, model_count: int, defender: Unit) -> Rolls:
    total_attacks = unit.weapon.attacks * model_count
    hits = Rolls(total_attacks, rolln(total_attacks))

    # if reroll_hit_1s in unit.traits or reroll_hit_1s in unit.weapon.traits:
    #     reroll_roll_amount = 1
    #     if GameSettings.REROLL_ALL_HITS:
    #         reroll_roll_amount = 0
    #     hits = reroll_hit_1s.calculation(hits, reroll_roll_amount)

    bs = unit.weapon.bs
    hits.successes = np.sum(hits.rolls >= bs)
    hits.failures = hits.attempts - hits.successes
    hits.ones = np.sum(hits.rolls == 1)
    hits.crits = np.sum(hits.rolls >= GameSettings.CRIT)

    if sustained_hits in unit.traits or sustained_hits in unit.weapon.traits:
        hits = sustained_hits.calculation(hits)

    if lethal_hits in unit.traits or lethal_hits in unit.weapon.traits:
        hits = lethal_hits.calculation(hits)

    hits.final_rolls = hits.rolls
    return hits
