from core.scenario import Scenario
from core.units import *
from config.constants import GameSettings
from utils.dice import rollx
from utils.calculations import (
    wound_roll_needed,
    save_roll_needed,
    count_success,
    count_equal_value_in_list,
    calculate_models_killed,
)
from core.rolls import Rolls
from typing import Optional
from core.traits import *


def run_multiple_simulations_for_average(simulations: int, scenario: Scenario) -> Scenario:
    for _ in range(simulations):
        scenario.defender_model_wounds = [scenario.defender[0].wounds] * scenario.defender[1]
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
    my_scenario.defender_model_wounds = [my_scenario.defender[0].wounds] * my_scenario.defender[1]

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
    scenario.total_damage += sum(wound_damage_list)
    scenario.total_damage_not_fnp += fnp.failures
    scenario.models_killed += models_killed
    scenario.defender_model_wounds = defender_remaining_wounds

    scenario.rolls_hits.extend_rolls(hits)
    scenario.rolls_wounds.extend_rolls(wounds)
    scenario.rolls_saves.extend_rolls(saves)
    scenario.rolls_fnp.extend_rolls(fnp)

    return scenario


def sim_hits(unit: Unit, model_count: int, defender: Unit) -> Rolls:
    total_attacks = unit.weapon.attacks * model_count
    hits = Rolls(total_attacks, rollx(total_attacks))
    
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


def sim_wounds(hits: Rolls, attacking_unit: Unit, defender: Unit) -> Rolls:
    wounds = Rolls(hits.successes, rollx(hits.successes))
    wounds.attempts = hits.successes

    wound_threshold = wound_roll_needed(
        attacking_unit.weapon.strength, defender.toughness
    )

    wounds.successes = count_success(wounds.rolls, wound_threshold)
    wounds.failures = wounds.attempts - wounds.successes
    wounds.ones = count_equal_value_in_list(wounds.rolls, 1)
    wounds.crits = count_success(wounds.rolls, GameSettings.CRIT)

    if lethal_hits in attacking_unit.traits or lethal_hits in attacking_unit.weapon.traits:
        wounds.successes += hits.crits

    wounds.final_rolls = wounds.rolls
    return wounds


def sim_saves(wounds: Rolls, attacking_unit: Unit, defender: Unit) -> Rolls:
    saves = Rolls(wounds.successes, rollx(wounds.successes))
    saves.attempts = wounds.successes

    save_threshold = save_roll_needed(
        (attacking_unit.weapon.ap + GameSettings.EXTRA_AP), defender.save, defender.invuln
    )

    saves.successes = count_success(saves.rolls, save_threshold)
    saves.failures = saves.attempts - saves.successes
    saves.ones = count_equal_value_in_list(saves.rolls, 1)
    saves.crits = count_equal_value_in_list(saves.rolls, GameSettings.CRIT)
    saves.final_rolls = saves.rolls
    return saves


def sim_fnp(saves: Rolls, attacking_unit: Unit, defender: Unit) -> Rolls:
    total_damage = saves.failures * attacking_unit.weapon.damage

    fnp = Rolls(total_damage, rollx(total_damage))

    fnp.successes = count_success(fnp.rolls, defender.fnp)
    fnp.failures = fnp.attempts - fnp.successes
    fnp.ones = count_equal_value_in_list(fnp.rolls, 1)
    fnp.crits = count_equal_value_in_list(fnp.rolls, GameSettings.CRIT)
    fnp.final_rolls = fnp.rolls
    return fnp


def sim_wound_damage_list(fnp: Rolls, attacking_unit: Unit) -> list[int]:
    wound_damage_list = []
    wounds_taken = fnp.failures // attacking_unit.weapon.damage
    fractional_wound = fnp.failures % attacking_unit.weapon.damage
    for _ in range(wounds_taken):
        wound_damage_list.append(attacking_unit.weapon.damage)
    if fractional_wound > 0:
        wound_damage_list.append(fractional_wound)
    return wound_damage_list


def sim_models_killed(
        wound_damage_list: list[int], defender: Unit, defender_model_wounds: list[int]
):
    models_killed, defender_remaining_wounds = calculate_models_killed(
        defender_model_wounds, wound_damage_list
    )
    return models_killed, defender_remaining_wounds
