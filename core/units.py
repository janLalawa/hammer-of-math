from core.abilities import generic_abilities
from core.abilities.ability_generic import *
from core.abilities.ability_base import Ability
from core.weapons import *

import core.abilities


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
            abilities: list[Ability] = None,
    ):
        if abilities is None:
            abilities = []
        self.name = name
        self.toughness = toughness
        self.save = save
        self.invuln = invuln
        self.fnp = fnp
        self.wounds = model_wounds
        self.weapon = weapon
        self.abilities = abilities

    def __str__(self):
        return f"{self.name}"


allarus_custodians = Unit(
    name="Allarus Custodians with Castellan Axes(Melee)",
    toughness=7,
    save=2,
    invuln=4,
    fnp=7,
    model_wounds=3,
    weapon=castellan_axe_m,
    abilities=[],
)

allarus_custodians_no_sustained = Unit(
    name="Allarus Custodians with Castellan Axes(Melee)",
    toughness=7,
    save=2,
    invuln=4,
    fnp=7,
    model_wounds=3,
    weapon=castellan_axe_m,
    abilities=[generic_abilities.available["Lethal Hits"]],
)

allarus_custodians_direct_mod = Unit(
    name="Allarus Custodians with Castellan Axes(Melee)",
    toughness=7,
    save=2,
    invuln=4,
    fnp=7,
    model_wounds=3,
    weapon=castellan_axe_m,
    abilities=[SustainedHits(1)],
)

ork_boyz = Unit(
    name="Ork Boyz with Choppas (Melee)",
    toughness=5,
    save=5,
    invuln=6,
    fnp=7,
    model_wounds=1,
    weapon=choppa_m,
)

teq = Unit(
    name=f"Terminator Equivalent",
    toughness=5,
    save=2,
    invuln=4,
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
    model_wounds=2,
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
    toughness=5,
    save=5,
    invuln=7,
    fnp=7,
    model_wounds=1,
    weapon=blank_weapon,
)

veq = Unit(
    name="Vehicle Equivalent",
    toughness=9,
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
