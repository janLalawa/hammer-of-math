from dataclasses import dataclass

from core.abilities.ability import Ability, AbilityCollection
from core.rolls import Rolls
from core.rollable import Rollable


@dataclass
class SustainedHits(Ability):
    def __init__(self, modifier: Rollable | int | None = 1):
        super().__init__(
            name=f"Sustained Hits {modifier}",
            description="Performs additional hits",
            modifier=modifier
        )

    def apply(self, hits: Rolls) -> Rolls:
        hits.successes += (self.modifier * hits.crits)
        return hits


@dataclass
class LethalHits(Ability):
    def __init__(self):
        super().__init__(
            name=f"Lethal Hits",
            description="Performs additional hits",
        )

    def apply(self, hits: Rolls) -> Rolls:
        hits.successes -= hits.crits
        return hits


@dataclass
class GenericAbilities(AbilityCollection):
    def __init__(self):
        super().__init__({
            "Sustained Hits": SustainedHits(),
            "Lethal Hits": LethalHits(),
        })

    available = {
        "Sustained Hits": SustainedHits(),
        "Lethal Hits": LethalHits(),
    }
