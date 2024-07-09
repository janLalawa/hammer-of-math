import csv
from config.constants import Paths
from core.scenario import Scenario


def write_results_to_csv(scenario_list: list[Scenario]) -> None:
    if not scenario_list:
        return

    with open(Paths.SIMULATION_RESULTS_PATH, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Attacker",
                "Defender",
                "Average Attacks",
                "Average Hits",
                "Average Wounds",
                "Average Unsaved Saves",
                "Average Damage",
                "Average Damage Not FNP",
                "Average Models Killed",
            ]
        )

        for scenario in scenario_list:
            attacker_names = ", ".join([attacker.model.name for attacker in scenario.attackers])

            writer.writerow(
                [
                    attacker_names,
                    scenario.defender.model.name,
                    scenario.average_attacks,
                    scenario.average_hits,
                    scenario.average_wounds,
                    scenario.average_unsaved_saves,
                    scenario.average_damage,
                    scenario.average_damage_not_fnp,
                    scenario.average_models_killed,
                ]
            )
