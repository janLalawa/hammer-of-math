import time

from core import *
from core.units import *
from sim.simulation import run_multiple_simulations_for_average, build_scenarios
from config.constants import GameSettings
from utils.csv_writer import write_results_to_csv
from graphing.sankey import create_sankey_from_scenario


def main():
    run_count = GameSettings.RUN_COUNT

    attackers = [
        [(custodian_guard, 5)],
        [(allarus_custodians, 5)],
        [(custodian_guard_lethal, 5)],
        [(custodian_guard_sustained, 5)],
    ]

    defenders = [meq, teq, ]

    scenario_list: list[Scenario] = build_scenarios(attackers, defenders)

    sim_list: list[Scenario] = []
    for current_scenario in scenario_list:
        this_sim = run_multiple_simulations_for_average(current_scenario, run_count)
        sim_list.append(this_sim)

    write_results_to_csv(sim_list)
    # create_sankey_from_scenario(scenario_list[0])


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Simulation took {time.time() - start_time} seconds")
