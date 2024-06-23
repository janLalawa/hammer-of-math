import logging
from functools import wraps
from utils.simulation_summary import simulation_summary
import numpy as np
from config.constants import Paths

logging.basicConfig(
    filename=Paths.SIMULATION_LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
sim_logger = logging.getLogger()


def format_rolls(rolls):
    return (
        f"Rolls: {rolls.rolls.tolist()},\n"
        f"Attempts: {rolls.attempts},\n"
        f"Successes: {rolls.successes},\n"
        f"Failures: {rolls.failures},\n"
        f"One Rolls: {rolls.ones},\n"
        f"Crit Rolls: {rolls.crits},\n"
        f"Final Rolls: {rolls.final_rolls.tolist()}\n"
    )


def format_rolls_summary(phase, summary):
    total_attempts = summary['attempts']
    success_rate = (summary['successes'] / total_attempts) * 100 if total_attempts > 0 else 0
    failure_rate = (summary['failures'] / total_attempts) * 100 if total_attempts > 0 else 0
    ones_rate = (summary['ones'] / total_attempts) * 100 if total_attempts > 0 else 0
    crits_rate = (summary['crits'] / total_attempts) * 100 if total_attempts > 0 else 0

    return (
        f"Phase: {phase},\n"
        f"Total Attempts: {total_attempts},\n"
        f"Total Successes: {summary['successes']} ({success_rate:.2f}%),\n"
        f"Total Failures: {summary['failures']} ({failure_rate:.2f}%),\n"
        f"Total One Rolls: {summary['ones']} ({ones_rate:.2f}%),\n"
        f"Total Crit Rolls: {summary['crits']} ({crits_rate:.2f}%)\n"
    )


def simulation_logger(granularity='summary', log_level=logging.INFO):
    def decorator(func):
        phase = func.__name__.split('_')[1]  # Extract the phase from the function name

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            attacker = args[0] if len(args) > 0 else None
            defender = args[2] if len(args) > 2 else None

            attacker_desc = f"{attacker}" if attacker else "Unknown Attacker"
            defender_desc = f"{defender}" if defender else "Unknown Defender"

            key = f"{attacker_desc} attacking {defender_desc}"
            simulation_summary[key][phase]['attempts'] += result.attempts
            simulation_summary[key][phase]['successes'] += result.successes
            simulation_summary[key][phase]['failures'] += result.failures
            simulation_summary[key][phase]['ones'] += result.ones
            simulation_summary[key][phase]['crits'] += result.crits

            if granularity == 'detailed':
                sim_logger.log(
                    log_level,
                    f"Function {func.__name__} called by {attacker_desc} attacking {defender_desc} with args: {args}, kwargs: {kwargs}, result:\n{format_rolls(result)}"
                )
            return result

        return wrapper

    return decorator


def log_simulation_summary():
    for key, phases in simulation_summary.items():
        for phase, summary in phases.items():
            sim_logger.info(f"{key} summary for {phase} phase:\n{format_rolls_summary(phase, summary)}")
