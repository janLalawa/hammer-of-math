import numpy as np

from config.constants import GameSettings
from core import Scenario
from core.abilities import Pos
from core.rolls import Rolls
from core.units import *
from utils.dice import rolln


def sim_hits_scenario(scenario: Scenario) -> Rolls:
    unit = scenario.attackers[0][0]
    model_count = scenario.attackers[0][1]
    defender = scenario.defender[0]
    return sim_hits(unit, model_count, defender)


def sim_hits(unit: Unit, model_count: int, defender: Unit) -> Rolls:
    total_attacks = unit.weapon.attacks * model_count
    hits = Rolls(total_attacks, rolln(total_attacks))

    bs = unit.weapon.bs
    hits.successes = np.sum(hits.rolls >= bs)
    hits.failures = hits.attempts - hits.successes
    hits.ones = np.sum(hits.rolls == 1)
    hits.crits = np.sum(hits.rolls >= GameSettings.CRIT)

    for trait in unit.abilities:
        if trait.position == Pos.HITS_APPLY_CRIT_EFFECTS:
            hits = trait.apply(hits)

    hits.final_rolls = hits.rolls
    return hits
