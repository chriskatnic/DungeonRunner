from character import *


class villain(character):

    def type(self):
        return "villain"

    def specialattack(self):
        self.printmessage("Villain performs special attack!")
        return 0
