import numpy as np
from core.rollable import Rollable


class Rolls:
    def __init__(
        self,
        attempts: Rollable = 0,
        rolls: np.array([]) = np.array([]),
        ones: int = 0,
        crits: int = 0,
        successes: int = 0,
        failures: int = 0,
        rerolled_rolls=None,
        final_rolls=None,
    ):
        self.attempts: Rollable = attempts
        self.rolls: np.array([]) = rolls
        self.ones: int = ones
        self.crits: int = crits
        self.successes: int = successes
        self.failures: int = failures
        self.rerolled_rolls: np.array([]) = (
            rerolled_rolls if rerolled_rolls is not None else np.array([])
        )
        self.final_rolls: np.array([]) = (
            final_rolls if final_rolls is not None else np.array([])
        )

    def __str__(self):
        return (
            f"Rolls: {self.rolls.tolist()},\n"
            f"Attempts: {self.attempts},\n"
            f"Successes: {self.successes},\n"
            f"Failures: {self.failures},\n"
            f"One Rolls: {self.ones},\n"
            f"Crit Rolls: {self.crits},\n"
            f"Final Rolls: {self.final_rolls.tolist()}\n"
        )

    def extend_rolls(self, rolls: "Rolls") -> None:
        self.rolls = np.concatenate((self.rolls, rolls.rolls))
        self.attempts += rolls.attempts
        self.ones += rolls.ones
        self.crits += rolls.crits
        self.successes += rolls.successes
        self.failures += rolls.failures
        self.rerolled_rolls = np.concatenate(
            (self.rerolled_rolls, rolls.rerolled_rolls)
        )
        self.final_rolls = np.concatenate((self.final_rolls, rolls.final_rolls))
