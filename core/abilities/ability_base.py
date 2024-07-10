from core.abilities.ability_positions import Pos, BattlePhase
from dataclasses import dataclass
from core.rollable import Rollable, RollableWrapper
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

    def unregister_ability(self, ability: Ability):
        if ability.name in self.available:
            del self.available[ability.name]

    def get_ability(self, ability_name: str) -> Ability | None:
        return self.available.get(ability_name, None)


def register_ability(ability_collection_instance: AbilityCollection, *args, modifier_list=None, **kwargs):
    def decorator(ability_cls):
        if modifier_list is None:
            instance = ability_cls(*args, **kwargs)
            ability_collection_instance.register_ability(instance)
        else:
            for modifier in modifier_list:
                if isinstance(modifier, RollableWrapper):
                    instance = ability_cls(modifier=modifier.rollable, *args, **kwargs)
                elif isinstance(modifier, str):
                    instance = ability_cls(modifier=Rollable(modifier), *args, **kwargs)
                else:
                    instance = ability_cls(modifier=modifier, *args, **kwargs)

                ability_collection_instance.register_ability(instance)
        return ability_cls

    return decorator
