from core.abilities.ability_positions import Pos, BattlePhase
from dataclasses import dataclass
from core.rollable import Rollable
import importlib
import pathlib


@dataclass
class Ability:
    name: str
    description: str
    modifier: int | Rollable = 0
    cost: int = 0
    position: Pos = Pos.POS_END
    active: bool = True

    def apply(self, *args, **kwargs):
        pass


def register_ability(ability_collection_instance):
    def decorator(ability_cls):
        instance = ability_cls()
        ability_collection_instance.register_ability(instance)
        return ability_cls

    return decorator


class AbilityCollection:
    available: dict[str, Ability]

    def __init__(self, abilities_dir=None):
        self.available = {}
        if abilities_dir:
            self.load_abilities_from_directory(abilities_dir)

    def load_abilities_from_directory(self, directory_path):
        for path in pathlib.Path(directory_path).rglob("*.py"):
            module_name = path.stem
            module_path = str(path).replace("/", ".").rstrip(".py")
            module = importlib.import_module(module_path)
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if isinstance(attribute, Ability):
                    self.register_ability(attribute)

    def register_ability(self, ability: Ability):
        self.available[ability.name] = ability
        self.available = {k: v for k, v in sorted(self.available.items(), key=lambda item: item[1].position.value)}

    def unregister_ability(self, ability: Ability):
        if ability.name in self.available:
            del self.available[ability.name]
            self.available = {k: v for k, v in sorted(self.available.items(), key=lambda item: item[1].position.value)}

    def get_ability(self, ability_name: str) -> Ability | None:
        return self.available.get(ability_name, None)
