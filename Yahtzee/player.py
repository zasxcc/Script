class Player:
    UPPER = 6   # upper category 6개
    LOWER = 7   # lower category 7개

    def __init__(self, name):
        self.name = name

        # 13개 category 점수
        self.scores = [0 for i in range(self.UPPER + self.LOWER)]
        # 13개 category 사용 여부
        self.used = [False for i in range(self.UPPER + self.LOWER)]

    def setScore(self, score, index):
        self.scores[index] = score

    def setAtUsed(self, index):
        self.used[index] = True

    def getUpperScore(self):
        lst = [self.scores[i] for i in range(0, 6)]
        return sum(lst)

    def getLowerScore(self):
        lst = [self.scores[i] for i in range(6, 13)]
        return sum(lst)

    def getUsed(self, index):
        return self.used[index]

    def toString(self):
        return self.name

    def allUpperUsed(self):
        # upper category 6개 모두 사용되었는가?
        # UpperScores, UpperBonus 계산에 활용
        for i in range(self.UPPER):
            if self.used[i] == False:
                return False
        return True

    def allLowerUsed(self):
        for i in range(6, self.LOWER + 6):
            if self.used[i] == False:
                return False
        return True



