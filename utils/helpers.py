from core import Scenario
from core.units import Unit, ModelGroup
import numpy as np

def build_scenarios(atk_list: list[Unit], def_group: list[ModelGroup]) -> list[Scenario]:
    current_scenarios = []
    for current_attacker in atk_list:
        for current_defender in def_group:
            current_scenarios.append(Scenario(current_attacker, current_defender))
    return current_scenarios

def make_json_serializable(obj):
    """Convert NumPy types to standard Python types for JSON serialization."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return {k: make_json_serializable(v) for k, v in obj.__dict__.items()
                if not k.startswith('_')}
    else:
        return obj