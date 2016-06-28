from random import randint


class character:
    def __init__(self, name="null", level=1, hitpoints=50):
        self.name = name
        self.level = level
        self.hitpoints = hitpoints

    def attack(self):
        return randint(3, 5) * self.level

    def defend(self, attack):
        damage = attack - randint(1, self.level)
        if damage < 0:
            damage = 0
        self.hitpoints -= damage
        return self.name + " takes " + str(damage) + " damage!"




    def alive(self):
        return self.hitpoints > 0

    def printmessage(self, message):
        print(message)