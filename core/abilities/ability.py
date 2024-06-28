from dataclasses import dataclass
from core.rolls import Rolls


@dataclass
class Ability:
    name: str
    description: str
    modifier: int
    cost: int = 0
    position: int = 999

    def apply(self, *args, **kwargs):
        pass


@dataclass
class SustainedHits(Ability):
    def __init__(self, modifier: int):
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
