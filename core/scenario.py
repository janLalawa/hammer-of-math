from typing import Optional

from core.rolls import Rolls
from core.units import Unit
import numpy as np
from config.constants import GameSettings


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
            rolls_hits: Rolls = None,
            rolls_wounds: Rolls = None,
            rolls_saves: Rolls = None,
            rolls_fnp: Rolls = None,
            average_attacks: float = 0,
            average_hits: float = 0,
            average_wounds: float = 0,
            average_unsaved: float = 0,
            average_damage: float = 0,
            average_damage_not_fnp: float = 0,
            average_models_killed: float = 0, ):
        if rolls_saves is None:
            rolls_saves = Rolls(0, np.array([]))
        if rolls_wounds is None:
            rolls_wounds = Rolls(0, np.array([]))
        if rolls_hits is None:
            rolls_hits = Rolls(0, np.array([]))
        if rolls_fnp is None:
            rolls_fnp = Rolls(0, np.array([]))
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
        self.rolls_hits = rolls_hits
        self.rolls_wounds = rolls_wounds
        self.rolls_saves = rolls_saves
        self.rolls_fnp = rolls_fnp
        self.average_attacks = average_attacks
        self.average_hits = average_hits
        self.average_wounds = average_wounds
        self.average_unsaved_saves = average_unsaved
        self.average_damage = average_damage
        self.average_damage_not_fnp = average_damage_not_fnp
        self.average_models_killed = average_models_killed

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

    def calculate_averages(self, run_count: int = GameSettings.RUN_COUNT):
        self.average_attacks = round(self.total_attacks / run_count, 2)
        self.average_hits = round(self.total_hits / run_count, 2)
        self.average_wounds = round(self.total_wounds / run_count, 2)
        self.average_unsaved_saves = round(self.total_unsaved_saves / run_count, 2)
        self.average_damage = round(self.total_damage / run_count, 2)
        self.average_damage_not_fnp = round(self.total_damage_not_fnp / run_count, 2)
        self.average_models_killed = round(self.models_killed / run_count, 2)

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

    def print_results(self, run_count: int = GameSettings.RUN_COUNT):
        print(f"------Results: {run_count} iterations--------")
        print(f"Total Attacks: {round(self.total_attacks / run_count, 2)}")
        print(f"Total Hits: {round(self.total_hits / run_count, 2)}")
        print(f"Total Wounds: {round(self.total_wounds / run_count, 2)}")
        print(f"Total Unsaved Saves: {round(self.total_unsaved_saves / run_count, 2)}")
        print(
            f"Total Damage Dealt: {round(self.total_damage / run_count, 2)} (over {round(len(self.wound_list) / run_count, 2)} wounds)")
        print(f"Total Not FNP: {round(self.total_damage_not_fnp / run_count, 2)}")
        print(f"Defender Models Killed: {round(self.models_killed / run_count, 2)}")
        print("-----------------End------------------")
