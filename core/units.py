from core.weapons import Weapon, guardian_spear_m, choppa_m, blank_weapon
from core.traits import *


class Unit:
    def __init__(
            self,
            name: str = "Unit",
            toughness: int = 7,
            save: int = 7,
            invuln: int = 7,
            fnp: int = 7,
            model_wounds: int = 1,
            weapon: Weapon = blank_weapon,
            traits=None,
    ):
        if traits is None:
            traits = []
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
    traits=[sustained_hits, lethal_hits],
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

teq = Unit(
    name=f"Terminator Equivalent",
    toughness=5,
    save=2,
    invuln=5,
    fnp=7,
    model_wounds=3,
    weapon=blank_weapon,
)

meq = Unit(
    name="Marine Equivalent",
    toughness=4,
    save=3,
    invuln=7,
    fnp=7,
    model_wounds=1,
    weapon=blank_weapon,
)

geq = Unit(
    name="Guard Equivalent",
    toughness=3,
    save=5,
    invuln=7,
    fnp=7,
    model_wounds=1,
    weapon=blank_weapon,
)

oeq = Unit(
    name="Ork Equivalent",
    toughness=4,
    save=6,
    invuln=7,
    fnp=7,
    model_wounds=1,
    weapon=blank_weapon,
)

veq = Unit(
    name="Vehicle Equivalent",
    toughness=7,
    save=3,
    invuln=7,
    fnp=7,
    model_wounds=10,
    weapon=blank_weapon,
)

hq = Unit(
    name="Hero/HQ Equivalent",
    toughness=4,
    save=2,
    invuln=4,
    fnp=7,
    model_wounds=5,
    weapon=blank_weapon,
)

mc = Unit(
    name="Monster/Monstrous Creature",
    toughness=7,
    save=3,
    invuln=5,
    fnp=7,
    model_wounds=8,
    weapon=blank_weapon,
)

troop = Unit(
    name="Troop Equivalent",
    toughness=4,
    save=3,
    invuln=7,
    fnp=7,
    model_wounds=1,
    weapon=blank_weapon,
)
