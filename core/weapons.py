class Weapon:
    def __init__(
            self,
            name: str,
            attacks: int,
            bs: int,
            strength: int,
            ap: int,
            damage: int,
            traits: list[str],
            weapon_range: int,
    ):
        self.name = name
        self.damage = damage
        self.attacks = attacks
        self.bs = bs
        self.strength = strength
        self.ap = ap
        self.traits = traits
        self.weapon_range = weapon_range  # Set to 0 for melee weapons

    def __str__(self):
        return self.name


# Example Weapons

blank_weapon = Weapon(
    name="Blank Weapon",
    attacks=1,
    bs=2,
    strength=1,
    ap=0,
    damage=1,
    traits=[],
    weapon_range=0,
)

guardian_spear_m = Weapon(
    name="Guardian Spear Melee",
    attacks=5,
    bs=2,
    strength=7,
    ap=-2,
    damage=2,
    traits=["Sustained Hits 1"],
    weapon_range=0,
)

choppa_m = Weapon(
    name="Choppa Melee",
    attacks=3,
    bs=3,
    strength=4,
    ap=-1,
    damage=1,
    traits=[],
    weapon_range=0,
)
