from dataclasses import dataclass


@dataclass
class Weapon:
    name: str
    attacks: int
    bs: int
    strength: int
    ap: int
    damage: int
    abilities: list[str]
    weapon_range: int

    def __str__(self):
        return self.name


class WeaponCollection:
    def __init__(self):
        self.available = {}

    def register_weapon(self, weapon: Weapon):
        self.available[weapon.name] = weapon

    def unregister_weapon(self, weapon: Weapon):
        if weapon.name in self.available:
            del self.available[weapon.name]

    def get_weapon(self, name: str) -> Weapon | None:
        return self.available.get(name)


def register_weapon(weapon_collection_instance: WeaponCollection):
    def decorator(cls):
        instance = cls()
        weapon_collection_instance.register_weapon(instance)
        return cls

    return decorator
