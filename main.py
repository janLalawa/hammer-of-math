import time

from core import *
from core.units import *
from sim.simulation import run_multiple_simulations_for_average
from config.constants import GameSettings
from utils.csv_writer import write_results_to_csv
from utils.helpers import build_scenarios


from core.rollable import Rollable


def main():
    run_count = GameSettings.RUN_COUNT

    attackers: list[Unit] = [
        Unit([ModelGroup(custodian_guard, 5)]),
    ]

    defenders: list[ModelGroup] = [
        ModelGroup(teq, 50),
    ]

    scenario_list: list[Scenario] = build_scenarios(attackers, defenders)

    sim_list: list[Scenario] = []
    for current_scenario in scenario_list:
        this_sim = run_multiple_simulations_for_average(current_scenario, run_count)
        sim_list.append(this_sim)

    write_results_to_csv(sim_list)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Simulation took {time.time() - start_time} seconds")
