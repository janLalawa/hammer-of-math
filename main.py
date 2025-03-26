import csv
import time
from fastapi import FastAPI
from core import *
from pydantic import BaseModel
from core.units import *
from sim.simulation import run_multiple_simulations_for_average
from config.constants import GameSettings
from config.constants import Paths
from utils.csv_writer import write_results_to_csv
from utils.helpers import build_scenarios
import core.units as units_module  # Import the module itself for dynamic access

from core.rollable import Rollable

app = FastAPI()

def get_model_by_name(model_name: str):
    """Dynamically get a model object from the units module by name."""
    try:
        return getattr(units_module, model_name)
    except AttributeError:
        return None

def simulate(attacker_type, number_of_attacker, defender_type, number_of_defenders):
    # Convert string model names to actual model objects
    if isinstance(attacker_type, str):
        attacker_model = get_model_by_name(attacker_type)
        if attacker_model is None:
            return {"error": f"Unknown attacker type: {attacker_type}"}
    else:
        attacker_model = attacker_type

    if isinstance(defender_type, str):
        defender_model = get_model_by_name(defender_type)
        if defender_model is None:
            return {"error": f"Unknown defender type: {defender_type}"}
    else:
        defender_model = defender_type

    run_count = GameSettings.RUN_COUNT
    attackers: list[Unit] = [
        Unit([ModelGroup(attacker_model, number_of_attacker)]),
    ]

    defenders: list[ModelGroup] = [
        ModelGroup(defender_model, number_of_defenders),
    ]

    scenario_list: list[Scenario] = build_scenarios(attackers, defenders)

    sim_list: list[Scenario] = []
    for current_scenario in scenario_list:
        this_sim = run_multiple_simulations_for_average(current_scenario, run_count)
        sim_list.append(this_sim)

    write_results_to_csv(sim_list)
    results = []
    with open(Paths.SIMULATION_RESULTS_PATH, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert string values to appropriate types
            numeric_row = {
                k: float(v) if k.startswith("Average") else v
                for k, v in row.items()
            }
            results.append(numeric_row)

    return results[0] if results else {"error": "No results found"}
@app.get("/")
def get_simulation(attacker_type="custodian_guard", number_of_attacker=5, defender_type="teq", number_of_defenders=50):
    return simulate(attacker_type, number_of_attacker, defender_type, number_of_defenders)

class SimulationRequest(BaseModel):
    attacker_type: str  # e.g., "custodian_guard"
    defender_type: str  # e.g., "teq"
    attacker_quantity: int
    defender_quantity: int

@app.post("/sim")
def run_simulation(request: SimulationRequest):
    return simulate(
        request.attacker_type,
        request.attacker_quantity,
        request.defender_type,
        request.defender_quantity
    )

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

    print(sim_list[0])


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Simulation took {time.time() - start_time} seconds")
