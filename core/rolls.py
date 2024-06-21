class Rolls:
    def __init__(
            self,
            attempts: int,
            rolls: list[int],
            ones: int = 0,
            crits: int = 0,
            successes: int = 0,
            failures: int = 0,
            rerolled_rolls=None,
            final_rolls=None,
    ):
        self.attempts = attempts
        self.rolls = rolls
        self.ones = ones
        self.crits = crits
        self.successes = successes
        self.failures = failures
        self.rerolled_rolls: list[int] = rerolled_rolls
        self.final_rolls: list[int] = final_rolls

    def __str__(self):
        return (
            f"Rolls: {self.rolls},\n"
            f"Attempts: {self.attempts},\n"
            f"Successes: {self.successes},\n"
            f"Failures: {self.failures},\n"
            f"One Rolls: {self.ones},\n"
            f"Crit Rolls: {self.crits},\n"
            f"Final Rolls: {self.final_rolls}\n"
        )

    def extend_rolls(self, rolls: 'Rolls') -> None:
        self.rolls.extend(rolls.rolls)
        self.attempts += rolls.attempts
        self.ones += rolls.ones
        self.crits += rolls.crits
        self.successes += rolls.successes
        self.failures += rolls.failures
        self.rerolled_rolls.extend(rolls.rerolled_rolls) if self.rerolled_rolls is not None else self.rerolled_rolls
        self.final_rolls.extend(rolls.final_rolls) if self.final_rolls is not None else self.final_rolls
