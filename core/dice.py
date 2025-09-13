import random

class Dice:
    def __init__(self, sides: int = 6):
        self.__sides = sides
        self.__last_roll = []

    def roll(self):
        die1 = random.randint(1, self.__sides)
        die2 = random.randint(1, self.__sides)
        if die1 == die2:
            self.__last_roll = [die1] * 4
        else:
            self.__last_roll = [die1, die2]
        return self.__last_roll

    def get_last_roll(self):
        return self.__last_roll

    def set_last_roll(self, roll):
        self.__last_roll = roll

    def get_sides(self):
        return self.__sides

    def set_sides(self, sides):
        self.__sides = sides
