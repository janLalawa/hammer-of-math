from config.constants import GameSettings
from core.traits import *
from core.units import *
from utils.calculations import (
    count_success,
    count_equal_value_in_list,
)
from utils.dice import rolln


def sim_hits(unit: Unit, model_count: int, defender: Unit) -> Rolls:
    total_attacks = unit.weapon.attacks * model_count
    hits = Rolls(total_attacks, rolln(total_attacks))

    if reroll_hit_1s in unit.traits or reroll_hit_1s in unit.weapon.traits:
        reroll_roll_amount = 1
        if GameSettings.REROLL_ALL_HITS:
            reroll_roll_amount = 0
        hits = reroll_hit_1s.calculation(hits, reroll_roll_amount)

    hits.successes = count_success(hits.rolls, unit.weapon.bs)
    hits.failures = hits.attempts - hits.successes
    hits.ones = count_equal_value_in_list(hits.rolls, 1)
    hits.crits = count_success(hits.rolls, GameSettings.CRIT)

    if sustained_hits in unit.traits or sustained_hits in unit.weapon.traits:
        hits = sustained_hits.calculation(hits)

    if lethal_hits in unit.traits or lethal_hits in unit.weapon.traits:
        hits = lethal_hits.calculation(hits)

    hits.final_rolls = hits.rolls
    return hits
