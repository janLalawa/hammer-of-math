import numpy as np

from core.scenario import Scenario
from core.units import *
from sim.apply_wounds import sim_wound_damage_list, sim_models_killed
from sim.fnp import sim_fnp
from sim.hits import sim_hits
from sim.saves import sim_saves
from sim.wounds import sim_wounds
from config.constants import GameSettings


def run_simulations(run_count, attacker, defenders: list[Unit]):
    scenarios = [(Scenario([attacker], (defender, 50)), defender.name) for defender in defenders]
    simulations = [run_multiple_simulations_for_average(run_count, scenario[0]) for scenario in scenarios]
    defender_names = [scenario[1] for scenario in scenarios]
    return simulations, defender_names


def record_results(run_count, attacker, simulations):
    new_result = [attacker.name]
    for sim in simulations:
        new_result.append(round(sim.total_damage_not_fnp / run_count, 1))
        new_result.append(round(sim.models_killed / run_count, 1))
    return new_result


def build_scenarios(attacker_list: list[list[tuple[Unit, int]]], defender_list) -> list[Scenario]:
    current_scenarios = []
    for current_attacker in attacker_list:
        for current_defender in defender_list:
            current_scenarios.append(Scenario(current_attacker, (current_defender, GameSettings.DEFENDER_COUNT)))
    return current_scenarios


def run_multiple_simulations_for_average(scenario: Scenario, run_count: int = GameSettings.RUN_COUNT) -> Scenario:
    for _ in range(run_count):
        scenario.defender_model_wounds = np.full(scenario.defender[1], scenario.defender[0].wounds)
        for unit, model_count in scenario.attackers:
            calculate_unit(unit, model_count, scenario)

    scenario.calculate_averages(run_count)

    return scenario


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

    # scenario.rolls_hits.extend_rolls(hits)
    # scenario.rolls_wounds.extend_rolls(wounds)
    # scenario.rolls_saves.extend_rolls(saves)
    # scenario.rolls_fnp.extend_rolls(fnp)

    return scenario
