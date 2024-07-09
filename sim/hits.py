import numpy as np

from config.constants import GameSettings
from core import Scenario
from core.abilities import Pos
from core.rolls import Rolls
from core.units import *
from utils.dice import rolln


def sim_hits_scenario(scenario: Scenario, atk_model_group: ModelGroup) -> Rolls:
    hits = scenario.rolls_hits
    hits.attempts = atk_model_group.model.weapon.attacks * atk_model_group.count
    hits.rolls = rolln(hits.attempts)

    bs = atk_model_group.model.weapon.bs
    hits.successes = np.sum(hits.rolls >= bs)
    hits.failures = hits.attempts - hits.successes
    hits.ones = np.sum(hits.rolls == 1)
    hits.crits = np.sum(hits.rolls >= GameSettings.CRIT)

    for trait in atk_model_group.model.abilities:
        if trait.position == Pos.HITS_APPLY_CRIT_EFFECTS:
            hits = trait.apply(hits)

    return hits
