import csv
import numpy as np
import time
import cProfile
import pstats

from core import *
from core.units import *
from simulation.sim import run_multiple_simulations_for_average, build_scenarios
from config.constants import GameSettings
from utils.csv_writer import write_results_to_csv
from graphing.sankey import create_sankey_from_scenario

import plotly.graph_objects as go


def main():
    run_count = GameSettings.RUN_COUNT

    attackers = [
        [(custodian_guard, 20)],
        [(allarus_custodians, 20)],
        [(custodian_guard_lethal, 20)],
        [(custodian_guard_sustained, 20)],
        [(custodian_guard_lethal_and_sustained, 20)],
        [(ork_boyz, 20)]
    ]

    defenders = [meq, teq, custodian_guard, oeq, geq, ]

    scenario_list: list[Scenario] = build_scenarios(attackers, defenders)

    sim_list: list[Scenario] = []
    for current_scenario in scenario_list:
        this_sim = run_multiple_simulations_for_average(current_scenario, run_count)
        sim_list.append(this_sim)

    write_results_to_csv(sim_list)
    # create_sankey_from_scenario(scenario_list[0])


def profile_main():
    cProfile.run('main()', 'profile_output')

    with open('profile_results.txt', 'w') as f:
        p = pstats.Stats('profile_output', stream=f)
        p.sort_stats('cumulative').print_stats()


if __name__ == "__main__":
    start_time = time.time()
    profile_main()
    print(f"Simulation took {time.time() - start_time} seconds")
