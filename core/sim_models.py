class Rolls:
    def __init__(
            self,
            attempts: int,
            rolls: list[int],
            one_rolls: int = 0,
            crit_rolls: int = 0,
            successes: int = 0,
            failures: int = 0,
            rerolled_rolls=None,
            final_rolls=None,
    ):
        self.attempts = attempts
        self.rolls = rolls
        self.one_rolls = one_rolls
        self.crit_rolls = crit_rolls
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
            f"One Rolls: {self.one_rolls},\n"
            f"Crit Rolls: {self.crit_rolls},\n"
            f"Final Rolls: {self.final_rolls}\n"
        )
