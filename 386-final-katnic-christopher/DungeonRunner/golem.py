from villain import *


class golem(villain):

    def __init__(self, level = 1):
        self.name = "Golem"
        self.hitpoints = 45+45*(level - 1  / 2)
        self.level = level

    def specialattack(self):
        self.printmessage("golem special attack: Boulder toss!")
        return randint(5, 9) + self.level

    def type(self):
        return "golem"