from core.units import Unit
from core.traits import Trait
from typing import Optional
from core.rolls import Rolls


class Scenario:
    def __init__(
            self,
            attacker: list[tuple[Unit, int]],
            defender: tuple[Unit, int],
            total_attacks: int = 0,
            total_hits: int = 0,
            total_wounds: int = 0,
            total_unsaved: int = 0,
            total_not_fnp: int = 0,
            total_damage: int = 0,
            models_killed: int = 0,
            defender_model_wounds=None,
            wound_list=None,
            global_mods: Optional[list[Trait]] = None,
            rolls_hits: Rolls = None,
            rolls_wounds: Rolls = None,
            rolls_saves: Rolls = None,
            rolls_fnp: Rolls = None
    ):
        if rolls_saves is None:
            rolls_saves = Rolls(0, [])
        if rolls_wounds is None:
            rolls_wounds = Rolls(0, [])
        if rolls_hits is None:
            rolls_hits = Rolls(0, [])
        if rolls_fnp is None:
            rolls_fnp = Rolls(0, [])
        if wound_list is None:
            wound_list = []
        if defender_model_wounds is None:
            defender_model_wounds = []
        self.attackers = attacker
        self.defender = defender
        self.total_attacks = total_attacks
        self.total_hits = total_hits
        self.total_wounds = total_wounds
        self.total_unsaved_saves = total_unsaved
        self.total_damage_not_fnp = total_not_fnp
        self.total_damage = total_damage
        self.models_killed = models_killed
        self.wound_list = wound_list
        self.defender_model_wounds = defender_model_wounds
        self.global_mods = global_mods
        self.rolls_hits = rolls_hits
        self.rolls_wounds = rolls_wounds
        self.rolls_saves = rolls_saves
        self.rolls_fnp = rolls_fnp

    def __str__(self):
        return (
            f"Scenario: {self.attackers} vs {self.defender}\n"
            f"Total Attacks: {self.total_attacks}\n"
            f"Total Hits: {self.total_hits}\n"
            f"Total Wounds: {self.total_wounds}\n"
            f"Total Unsaved Saves: {self.total_unsaved_saves}\n"
            f"Total Damage Dealt: {self.total_damage} (over {len(self.wound_list)} wounds)\n"
            f"Total Not FNP: {self.total_damage_not_fnp}\n"
            f"Defender Models Killed: {self.models_killed}\n"
        )

    def print_units_short(self):
        print("------------Attackers-------------")
        for unit in self.attackers:
            model, count = unit
            print(f"{model.name} x{count} with {model.weapon.name}")

        print("------------Defender-------------")
        model, count = self.defender
        print(f"{model.name} x{count}")

    def print_units(self):
        print("------------Attackers-------------")
        for unit in self.attackers:
            model, count = unit
            print(f"{model.name} x{count} with {model.weapon.name}")
            print(f"Total Attacks: {model.weapon.attacks * count}")
            print(f"To Hit: {model.weapon.bs}+")
            print(f"Strength: {model.weapon.strength}")
            print(f"AP: {model.weapon.ap}")
            print(f"Damage: {model.weapon.damage}\n")

        print("------------Defender-------------")
        model, count = self.defender
        print(f"{model.name} x{count}")
        print(f"Toughness: {model.toughness}")
        print(f"Save: {model.save}+")
        print(f"Invuln: {model.invuln}+")
        print(f"FNP: {model.fnp}+")
        print(f"Wounds per model: {model.wounds} ({model.wounds * count} Total)\n")

    def print_rolls(self):
        print("-----------------Hits-----------------")
        print(self.rolls_hits)
        print("-----------------Wounds-----------------")
        print(self.rolls_wounds)
        print("-----------------Saves-----------------")
        print(self.rolls_saves)
        print("-----------------FNP-----------------")
        print(self.rolls_fnp)
        print("-----------------Wound Damage List-----------------")
        print(self.wound_list)
