import numpy as np

from core.scenario import Scenario
from core.units import *
from simulation.apply_wounds import sim_wound_damage_list, sim_models_killed
from simulation.fnp import sim_fnp
from simulation.hits import sim_hits
from simulation.saves import sim_saves
from simulation.wounds import sim_wounds


def run_multiple_simulations_for_average(simulations: int, scenario: Scenario) -> Scenario:
    for _ in range(simulations):
        scenario.defender_model_wounds = np.full(scenario.defender[1], scenario.defender[0].wounds)
        for unit, model_count in scenario.attackers:
            calculate_unit(unit, model_count, scenario)
    scenario.average_attacks = scenario.total_attacks / simulations
    scenario.average_hits = scenario.total_hits / simulations
    scenario.average_wounds = scenario.total_wounds / simulations
    scenario.average_unsaved_saves = scenario.total_unsaved_saves / simulations
    scenario.average_damage = scenario.total_damage / simulations
    scenario.average_damage_not_fnp = scenario.total_damage_not_fnp / simulations
    scenario.average_models_killed = scenario.models_killed / simulations

    return scenario


def run_simulation():
    # Example Scenario
    my_scenario = Scenario([(allarus_custodians, 3)], (teq, 5))
    my_scenario.defender_model_wounds = np.full(my_scenario.defender[1], my_scenario.defender[0].wounds)

    for unit, model_count in my_scenario.attackers:
        calculate_unit(unit, model_count, my_scenario)


def calculate_unit(unit: Unit, model_count: int, scenario: Scenario) -> Scenario:
    hits = sim_hits(unit, model_count, scenario.defender[0])
    wounds = sim_wounds(hits, unit, scenario.defender[0])
    saves = sim_saves(wounds, unit, scenario.defender[0])
    fnp = sim_fnp(saves, unit, scenario.defender[0])
    wound_damage_list = sim_wound_damage_list(fnp, unit)
    scenario.wound_list.extend(wound_damage_list)

    models_killed, defender_remaining_wounds = sim_models_killed(wound_damage_list, scenario.defender[0],
                                                                 scenario.defender_model_wounds)

    scenario.total_attacks += unit.weapon.attacks * model_count
    scenario.total_hits += hits.successes
    scenario.total_wounds += wounds.successes
    scenario.total_unsaved_saves += saves.failures
    scenario.total_damage += np.sum(wound_damage_list)
    scenario.total_damage_not_fnp += fnp.failures
    scenario.models_killed += models_killed
    scenario.defender_model_wounds = defender_remaining_wounds

    scenario.rolls_hits.extend_rolls(hits)
    scenario.rolls_wounds.extend_rolls(wounds)
    scenario.rolls_saves.extend_rolls(saves)
    scenario.rolls_fnp.extend_rolls(fnp)

    return scenario
