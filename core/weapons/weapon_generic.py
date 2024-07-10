from .weapon_base import Weapon, register_weapon, WeaponCollection


class GenericWeapons(WeaponCollection):
    pass


generic_weapons = GenericWeapons()


@register_weapon(generic_weapons)
class BlankWeapon(Weapon):
    def __init__(self):
        super().__init__(
            name="Blank Weapon",
            attacks=1,
            bs=2,
            strength=1,
            ap=0,
            damage=1,
            abilities=[],
            weapon_range=0,
        )


@register_weapon(generic_weapons)
class GuardianSpearMelee(Weapon):
    def __init__(self):
        super().__init__(
            name="Guardian Spear Melee",
            attacks=5,
            bs=2,
            strength=7,
            ap=-2,
            damage=2,
            abilities=[],
            weapon_range=0,
        )
