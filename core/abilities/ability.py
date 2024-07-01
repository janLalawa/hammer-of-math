from dataclasses import dataclass
from core.rolls import Rolls
from core.rollable import Rollable


@dataclass
class Ability:
    name: str
    description: str
    modifier: int | Rollable = 0
    cost: int = 0
    position: int = 999

    def apply(self, *args, **kwargs):
        pass


@dataclass
class AbilityCollection:
    available: dict[str, Ability]

    def __init__(self, available: dict[str, Ability]):
        self.available = available
        self.available = {k: v for k, v in sorted(self.available.items(), key=lambda item: item[1].position)}

    def __contains__(self, item):
        return item in self.available

    def __call__(self, *args, **kwargs):
        return self.available

    def __getitem__(self, item):
        return self.available[item]

    def __iter__(self):
        return iter(self.available.values())

    def __len__(self):
        return len(self.available)

    def __str__(self):
        return str(self.available)

    def register_ability(self, ability: Ability):
        self.available[ability.name] = ability
        self.available = {k: v for k, v in sorted(self.available.items(), key=lambda item: item[1].position)}

    def unregister_ability(self, ability: Ability):
        del self.available[ability.name]
        self.available = {k: v for k, v in sorted(self.available.items(), key=lambda item: item[1].position)}
