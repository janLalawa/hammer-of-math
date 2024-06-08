from core.weapons import guardian_spear_m, choppa_m


class Unit:
    def __init__(
            self,
            name: str = "Unit",
            toughness: int = 7,
            save: int = 7,
            invuln: int = 7,
            fnp: int = 7,
            model_wounds: int = 1,
            weapon=None,
            traits=None,
    ):
        self.name = name
        self.toughness = toughness
        self.save = save
        self.invuln = invuln
        self.fnp = fnp
        self.wounds = model_wounds
        self.weapon = weapon
        self.traits = traits

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


# Example Units

allarus_custodians = Unit(
    name="Allarus Custodians with Guardian Spears (Melee)",
    toughness=7,
    save=2,
    invuln=4,
    fnp=7,
    model_wounds=3,
    weapon=guardian_spear_m,
)

ork_boyz = Unit(
    name="Ork Boyz with Choppas (Melee)",
    toughness=5,
    save=5,
    invuln=5,
    fnp=5,
    model_wounds=1,
    weapon=choppa_m,
)
