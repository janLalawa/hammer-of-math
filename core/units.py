from dataclasses import dataclass

from core.abilities import generic_abilities
from core.abilities.ability_generic import *
from core.abilities.ability_base import Ability
from core.weapons import *

import core.abilities


@dataclass
class Model:
    def __init__(
        self,
        name: str = "Unit",
        toughness: int = 7,
        save: int = 7,
        invuln: int = 7,
        fnp: int = 7,
        model_wounds: int = 1,
        weapons=None,
        abilities: list[Ability] = None,
    ):
        if weapons is None:
            weapons = [blank_weapon]
        if abilities is None:
            abilities = []
        self.name = name
        self.toughness = toughness
        self.save = save
        self.invuln = invuln
        self.fnp = fnp
        self.wounds = model_wounds
        self.weapons = weapons
        self.abilities = abilities

    def __str__(self):
        return f"{self.name}"


@dataclass
class ModelGroup:
    model: Model
    count: int


@dataclass
class Unit:
    model_groups: list[ModelGroup]
    abilities: list[Ability] = None

    def __iter__(self):
        return iter(self.model_groups)


allarus_custodians = Model(
    name="Allarus Custodians with Castellan Axes(Melee)",
    toughness=7,
    save=2,
    invuln=4,
    fnp=7,
    model_wounds=3,
    weapons=[castellan_axe_m],
    abilities=[],
)

allarus_custodians_no_sustained = Model(
    name="Allarus Custodians with Castellan Axes(Melee)",
    toughness=7,
    save=2,
    invuln=4,
    fnp=7,
    model_wounds=3,
    weapons=[castellan_axe_m],
    abilities=[generic_abilities.available["Lethal Hits"]],
)

allarus_custodians_direct_mod = Model(
    name="Allarus Custodians with Castellan Axes(Melee)",
    toughness=7,
    save=2,
    invuln=4,
    fnp=7,
    model_wounds=3,
    weapons=[castellan_axe_m],
    abilities=[SustainedHits(1)],
)

custodian_guard = Model(
    name="Custodian Guard with Guardian Spears(Melee)",
    toughness=6,
    save=2,
    invuln=4,
    fnp=7,
    model_wounds=3,
    weapons=[guardian_spear_m, castellan_axe_m],
    abilities=[SustainedHits(1)],
)


ork_boyz = Model(
    name="Ork Boyz with Choppas (Melee)",
    toughness=5,
    save=5,
    invuln=6,
    fnp=7,
    model_wounds=1,
    weapons=[choppa_m],
)

teq = Model(
    name=f"Terminator Equivalent",
    toughness=5,
    save=2,
    invuln=4,
    fnp=7,
    model_wounds=3,
    weapons=[blank_weapon],
)

meq = Model(
    name="Marine Equivalent",
    toughness=4,
    save=3,
    invuln=7,
    fnp=7,
    model_wounds=2,
    weapons=[blank_weapon],
)

geq = Model(
    name="Guard Equivalent",
    toughness=3,
    save=5,
    invuln=7,
    fnp=7,
    model_wounds=1,
    weapons=[blank_weapon],
)

oeq = Model(
    name="Ork Equivalent",
    toughness=5,
    save=5,
    invuln=7,
    fnp=7,
    model_wounds=1,
    weapons=[blank_weapon],
)

veq = Model(
    name="Vehicle Equivalent",
    toughness=9,
    save=3,
    invuln=7,
    fnp=7,
    model_wounds=10,
    weapons=[blank_weapon],
)

hq = Model(
    name="Hero/HQ Equivalent",
    toughness=4,
    save=2,
    invuln=4,
    fnp=7,
    model_wounds=5,
    weapons=[blank_weapon],
)

mc = Model(
    name="Monster/Monstrous Creature",
    toughness=7,
    save=3,
    invuln=5,
    fnp=7,
    model_wounds=8,
    weapons=[blank_weapon],
)

troop = Model(
    name="Troop Equivalent",
    toughness=4,
    save=3,
    invuln=7,
    fnp=7,
    model_wounds=1,
    weapons=[blank_weapon],
)
