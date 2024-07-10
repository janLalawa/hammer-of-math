from dataclasses import dataclass
from enum import Enum
from typing import Union
from utils.dice import rolln


class ValueType(Enum):
    INT = 0
    DICE = 1
    FORMULA = 2


class Rollable:
    """
    This class is used to parse a value to be used for attacks, damage, abilities, etc.
    @param i: The input value to parse.
    Integers are returned as is. Example: 5 -> 5
    Strings in dice roll format are parsed as dice. Example: "2d6" -> [3, 6]
    String in format "x + y" are calculated individually, including dice. Example: "2d6 + 3" -> [3, 6] + 3
    """

    def __init__(self, i: int | str, frozen: bool = False, use_average: bool = False):
        self.input = i
        self.string_parsed: bool = False
        self.format: ValueType
        self.type = type(i)
        self.num_dice: int = 0
        self.sides: int = 0
        self.constant: int = 0
        self.last_roll: int = 0
        self.frozen: bool = False
        self.use_average: bool = False

        if isinstance(i, int):
            self.format = ValueType.INT
        elif isinstance(i, str):
            if "+" in i:
                self.format = ValueType.FORMULA
            elif "d" in i:
                self.format = ValueType.DICE
            else:
                raise ValueError("Invalid string format")
        else:
            raise TypeError("Unsupported type for Value")

        if self.format in {ValueType.DICE, ValueType.FORMULA}:
            self._parse_string()

    def clone(self):
        """
        Creates a new instance of Rollable with the same initial parameters,
        allowing for the use of the modifier without an immediate roll.
        """
        return Rollable(self.input, self.frozen, self.use_average)

    def _parse_string(self):
        if self.format == ValueType.DICE:
            parts = self.input.split("d")
            self.num_dice = int(parts[0])
            self.sides = int(parts[1])

        if self.format == ValueType.FORMULA:
            parts = self.input.split("+")
            dice_part = parts[0].strip()
            self.constant = int(parts[1].strip())

            dice_parts = dice_part.split("d")
            self.num_dice = int(dice_parts[0])
            self.sides = int(dice_parts[1])

        self.string_parsed = True

    def rollv(self) -> int | float:
        if self.frozen:
            return self.last_roll

        if self.use_average:
            return self.average()

        if self.format == ValueType.INT:
            self.last_roll = int(self.input)
            return self.last_roll

        if self.format == ValueType.DICE:
            result = sum(rolln(self.num_dice, self.sides))
            self.last_roll = int(result)
            return self.last_roll

        if self.format == ValueType.FORMULA:
            result = sum(rolln(self.num_dice, self.sides)) + self.constant
            self.last_roll = int(result)
            return self.last_roll

    def average(self) -> float:
        if self.format == ValueType.INT:
            return self.input

        if self.format == ValueType.DICE:
            return self.num_dice * (self.sides + 1) / 2

        if self.format == ValueType.FORMULA:
            return self.num_dice * (self.sides + 1) / 2 + self.constant

    def __mul__(self, other: int) -> int | float:
        if not isinstance(other, int):
            raise TypeError(f"Multiplication with type {type(other)} is not supported")

        total = 0
        for _ in range(other):
            total += self.rollv()
        return total

    def __rmul__(self, other: int) -> int | float:
        return self.__mul__(other)

    def __add__(self, other):
        return self.rollv() + other

    def __radd__(self, other):
        return self.rollv() + other

    def __sub__(self, other):
        return self.rollv() - other

    def __rsub__(self, other):
        return other - self.rollv()

    def __str__(self):
        return str(self.input)

    def __repr__(self):
        return str(self.input)

    def __int__(self):
        return self.rollv()

    def __float__(self):
        return float(self.rollv())

    def __eq__(self, other):
        return self.rollv() == other

    def __ne__(self, other):
        return self.rollv() != other

    def __lt__(self, other):
        return self.rollv() < other

    def __le__(self, other):
        return self.rollv() <= other

    def __gt__(self, other):
        return self.rollv() > other

    def __ge__(self, other):
        return self.rollv() >= other


class RollableWrapper:
    def __init__(self, name: str | int):
        self.name = name
        self.rollable = Rollable(name)
