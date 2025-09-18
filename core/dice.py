import random
from typing import List, Tuple

class Dice:

    def __init__(self, sides: int = 6) -> None:
        self.__sides: int = sides
        self.__last_roll: Tuple[int, int] = (1, 1)

    def roll(self) -> Tuple[int, int]:
        die1 = random.randint(1, self.__sides)
        die2 = random.randint(1, self.__sides)
        self.__last_roll = (die1, die2)
        return self.__last_roll

    def get_last_roll(self) -> Tuple[int, int]:
        return self.__last_roll

    def set_last_roll(self, roll: Tuple[int, int]) -> None:
        self.__last_roll = roll

    def get_sides(self) -> int:
        return self.__sides

    def set_sides(self, sides: int) -> None:
        self.__sides = sides

    def is_double(self, roll: Tuple[int, int]) -> bool:
        return roll[0] == roll[1]

    def get_moves(self, roll: Tuple[int, int]) -> List[int]:
        if self.is_double(roll):
            return [roll[0]] * 4
        return list(roll)
