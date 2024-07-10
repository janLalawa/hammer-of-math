import numpy as np

from config.constants import GameSettings
from core import Scenario
from core.abilities import Pos
from core.rolls import Rolls
from core.units import *
from utils.dice import rolln


def sim_hits_scenario(scenario: Scenario, atk_model_group: ModelGroup, wep_idx: int = 0) -> Rolls:
    hits = scenario.rolls_hits
    hits.attempts = atk_model_group.model.weapons[wep_idx].attacks * atk_model_group.count
    hits.rolls = rolln(hits.attempts)

    bs = atk_model_group.model.weapons[wep_idx].bs
    hits.successes = np.sum(hits.rolls >= bs)
    hits.failures = hits.attempts - hits.successes
    hits.ones = np.sum(hits.rolls == 1)
    hits.crits = np.sum(hits.rolls >= GameSettings.CRIT)

    for ability in atk_model_group.model.abilities:
        if ability.position == Pos.HITS_APPLY_CRIT_EFFECTS:
            hits = ability.apply(hits)

    return hits
