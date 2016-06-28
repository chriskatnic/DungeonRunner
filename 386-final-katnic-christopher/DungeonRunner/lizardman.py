from villain import *


class lizardman(villain):

    def __init__(self, level = 1):
        self.name = "Lizard Man"
        self.hitpoints = 35+35*(level - 1  / 2)
        self.level = level

    def specialattack(self):
        self.printmessage("lizardman special attack: Reptile strike!")
        return randint(3, 7) + self.level

    def type(self):
        return "lizardman"
