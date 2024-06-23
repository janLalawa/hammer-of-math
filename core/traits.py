from enum import Enum
from typing import Optional, Callable
from core.rolls import Rolls
from utils.dice import roll


class TraitType(Enum):
    WEAPON = 0
    ABILITY = 1
    STRATAGEM = 2
    DETACHMENT = 3
    ARMY_RULE = 4


class Trait:
    def __init__(
            self,
            name: str,
            trait_type: TraitType,
            description: str,
            calculation: Callable,
            modifier: Optional[int] = None,
    ):
        self.name = name
        self.trait_type = trait_type
        self.description = description
        self.calculation = calculation
        self.modifier = modifier

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def sustained_hits_calculation(hits: Rolls) -> Rolls:
    hits.successes += hits.crits
    return hits


def lethal_hits_calculation(hits: Rolls) -> Rolls:
    hits.successes -= hits.crits
    return hits

def reroll_1s_calculation(hits: Rolls, amount: int = 0) -> Rolls:
    if amount == 0:
        hits.rolls = [roll() if value == 1 else value for value in hits.rolls]
        return hits
    else:
        rerolled = 0
        for index, value in enumerate(hits.rolls):
            if value == 1 and rerolled < amount:
                hits.rolls[index] = roll()
                rerolled += 1
    return hits


sustained_hits = Trait(
    name="Sustained Hits",
    trait_type=TraitType.WEAPON,
    description="This weapon generates an additional hit on a critical hit.",
    calculation=sustained_hits_calculation,
)

lethal_hits = Trait(
    name="Lethal Hits",
    trait_type=TraitType.WEAPON,
    description="This weapon generates an additional hit on a critical hit.",
    calculation=lethal_hits_calculation,
)

reroll_hit_1s = Trait(
    name="Reroll 1s to Hit",
    trait_type=TraitType.ABILITY,
    description="This unit can reroll 1s to hit.",
    calculation=reroll_1s_calculation,
)

martial_mastery_crit = Trait(
    name="Martial Mastery (Crit)",
    trait_type=TraitType.ABILITY,
    description="This unit generates critical hits on a roll of 5 or 6 in melee",
    calculation=sustained_hits_calculation,
)
