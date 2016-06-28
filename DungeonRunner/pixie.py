from villain import *


class pixie(villain):

    def __init__(self, level = 1):
        self.name = "Pixie"
        self.hitpoints = 25 + 1*(level - 1  / 2)
        self.level = level

    def specialattack(self):
        self.printmessage("pixie special attack: sparkle glitter!")
        return randint(2, 5) + self.level

    def type(self):
        return "pixie"