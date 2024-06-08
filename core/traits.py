from enum import Enum
from typing import Optional


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
            calculation: Optional[str] = None,
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


sustained_hits = Trait(
    name="Sustained Hits",
    trait_type=TraitType.WEAPON,
    description="This weapon generates an additional hit on a critical hit.",
)

print(sustained_hits)  # This will print: Sustained Hits
print(repr(sustained_hits))  # This will print: Sustained Hits
