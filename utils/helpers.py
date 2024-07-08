from core import Scenario
from core.units import Unit, ModelGroup


def build_scenarios(atk_list: list[Unit], def_group: list[ModelGroup]) -> list[Scenario]:
    current_scenarios = []
    for current_attacker in atk_list:
        for current_defender in def_group:
            current_scenarios.append(Scenario(current_attacker, current_defender))
    return current_scenarios
