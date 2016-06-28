from character import *


class player(character):
    def heal(self):
        self.hitpoints += 3 * self.level + 3
        return "Player heals! " + str(self.hitpoints - (3 * self.level + 3)) + " -> " + str(self.hitpoints)

    def levelup(self):
        self.level += 1
        self.hitpoints += 15

    def attack(self):
        return randint(3, 5) * (self.level + 1)