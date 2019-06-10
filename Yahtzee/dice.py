from random import *


class Dice:
    def rollDie(self):
        self.roll = randint(1, 6)   # 1~6 랜덤 정수

    def getRoll(self):
        return self.roll

