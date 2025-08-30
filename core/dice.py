import random

class Dice:
    def __init__(self, sides: int = 6):
        self.sides = sides
        self.last_roll = []

    def roll(self):
        die1 = random.randint(1, self.sides)
        die2 = random.randint(1, self.sides)
        self.last_roll = [die1, die2]
        
        if die1 == die2:
            self.last_roll = [die1, die1, die1, die1]

        return self.last_roll

    def get_last_roll(self):
        return self.last_roll
