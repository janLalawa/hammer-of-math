from core.scenario import Scenario
from core.units import Unit, allarus_custodians, ork_boyz
from config.constants import GameSettings
from utils.dice import rollx
from utils.calculations import (
    wound_roll_needed,
    save_roll_needed,
    count_success,
    count_equal_value_in_list,
    calculate_models_killed,
)
from core.sim_models import Rolls
from typing import Optional


def run_simulation():
    # Example Scenario
    my_scenario = Scenario([(allarus_custodians, 3)], (ork_boyz, 20))
    my_scenario.defender_model_wounds = [1] * 20
    my_scenario.print_units()

    for unit, model_count in my_scenario.attackers:
        calculate_unit(unit, model_count, my_scenario)

    print()
    print("-----------------Results----------------")
    print(my_scenario)


def calculate_unit(unit: Unit, model_count: int, scenario: Scenario) -> Scenario:
    hits = sim_hits(unit, model_count, scenario.defender[0])
    print("-----------------Hits-----------------")
    print(hits)

    wounds = sim_wounds(hits, unit, scenario.defender[0])
    print("-----------------Wounds-----------------")
    print(wounds)

    saves = sim_saves(wounds, unit, scenario.defender[0])
    print("-----------------Saves-----------------")
    print(saves)

    fnp = sim_fnp(saves, unit, scenario.defender[0])
    print("-----------------FNP-----------------")
    print(fnp)

    wound_damage_list = sim_wound_damage_list(fnp, unit)
    print("-----------------Wound Damage List-----------------")
    print(wound_damage_list)
    scenario.wound_list.extend(wound_damage_list)

    models_killed, defender_remaining_wounds = sim_models_killed(
        wound_damage_list, scenario.defender[0], scenario.defender_model_wounds
    )

    scenario.total_attacks += unit.weapon.attacks * model_count
    scenario.total_hits += hits.successes
    scenario.total_wounds += wounds.successes
    scenario.total_unsaved_saves += saves.failures
    scenario.total_damage += sum(wound_damage_list)
    scenario.total_damage_not_fnp += fnp.failures
    scenario.models_killed += models_killed
    scenario.defender_model_wounds = defender_remaining_wounds

    return scenario


def sim_hits(unit: Unit, model_count: int, defender: Unit) -> Rolls:
    total_attacks = unit.weapon.attacks * model_count
    hits = Rolls(total_attacks, rollx(total_attacks))
    hits.successes = count_success(hits.rolls, unit.weapon.bs)
    hits.failures = hits.attempts - hits.successes
    hits.one_rolls = count_equal_value_in_list(hits.rolls, 1)
    hits.crit_rolls = count_equal_value_in_list(hits.rolls, GameSettings.CRIT)
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
    wounds.one_rolls = count_equal_value_in_list(wounds.rolls, 1)
    wounds.crit_rolls = count_equal_value_in_list(wounds.rolls, GameSettings.CRIT)
    wounds.final_rolls = wounds.rolls
    return wounds


def sim_saves(wounds: Rolls, attacking_unit: Unit, defender: Unit) -> Rolls:
    saves = Rolls(wounds.successes, rollx(wounds.successes))
    saves.attempts = wounds.successes

    save_threshold = save_roll_needed(
        attacking_unit.weapon.ap, defender.save, defender.invuln
    )

    saves.successes = count_success(saves.rolls, save_threshold)
    saves.failures = saves.attempts - saves.successes
    saves.one_rolls = count_equal_value_in_list(saves.rolls, 1)
    saves.crit_rolls = count_equal_value_in_list(saves.rolls, GameSettings.CRIT)
    saves.final_rolls = saves.rolls
    return saves


def sim_fnp(saves: Rolls, attacking_unit: Unit, defender: Unit) -> Rolls:
    total_damage = saves.failures * attacking_unit.weapon.damage

    fnp = Rolls(total_damage, rollx(total_damage))

    fnp.successes = count_success(fnp.rolls, defender.fnp)
    fnp.failures = fnp.attempts - fnp.successes
    fnp.one_rolls = count_equal_value_in_list(fnp.rolls, 1)
    fnp.crit_rolls = count_equal_value_in_list(fnp.rolls, GameSettings.CRIT)
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
