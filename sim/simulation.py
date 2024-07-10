import numpy as np

from core import Rolls
from core.scenario import Scenario
from core.units import *
from sim.apply_wounds import sim_wound_damage_list, sim_models_killed
from sim.fnp import sim_fnp_scenario
from sim.hits import sim_hits_scenario
from sim.saves import sim_saves_scenario
from sim.wounds import sim_wounds_scenario
from config.constants import GameSettings


def run_multiple_simulations_for_average(scenario: Scenario, run_count: int = GameSettings.RUN_COUNT) -> Scenario:

    for _ in range(run_count):
        scenario.defender_model_wounds = np.full(scenario.defender.count, scenario.defender.model.wounds)

        for model_group in scenario.attackers.model_groups:
            for wep_idx in range(len(model_group.model.weapons)):
                simulate_model_group_for_weapon(model_group, wep_idx, scenario)

    scenario.calculate_averages(run_count)

    return scenario


def simulate_model_group_for_weapon(model_group: ModelGroup, wep_idx: int, scenario: Scenario) -> Scenario:
    scenario.rolls_hits = Rolls()
    scenario.rolls_wounds = Rolls()
    scenario.rolls_saves = Rolls()
    scenario.rolls_fnp = Rolls()

    scenario.rolls_hits = sim_hits_scenario(scenario, model_group, wep_idx)
    scenario.rolls_wounds = sim_wounds_scenario(scenario, model_group, wep_idx)
    scenario.rolls_saves = sim_saves_scenario(scenario, model_group, wep_idx)
    scenario.rolls_fnp = sim_fnp_scenario(scenario, model_group, wep_idx)

    wound_damage_list = sim_wound_damage_list(scenario.rolls_fnp, model_group.model)
    scenario.wound_list.extend(wound_damage_list)

    models_killed, defender_remaining_wounds = sim_models_killed(
        wound_damage_list, scenario.defender.model, scenario.defender_model_wounds
    )

    scenario.total_attacks += model_group.model.weapons[wep_idx].attacks * model_group.count
    scenario.total_hits += scenario.rolls_hits.successes
    scenario.total_wounds += scenario.rolls_wounds.successes
    scenario.total_unsaved_saves += scenario.rolls_saves.failures
    scenario.total_damage += np.sum(wound_damage_list)
    scenario.total_damage_not_fnp += scenario.rolls_fnp.failures
    scenario.models_killed += models_killed
    scenario.defender_model_wounds = defender_remaining_wounds

    return scenario
