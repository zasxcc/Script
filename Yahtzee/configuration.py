from dice import *


class Configuration:
    configs =  ["Category","Ones", "Twos","Threes","Fours","Fives","Sixes", "Upper Scores",
               "Upper Bonus(35)","Three of a kind", "Four of a kind", "Full House(25)",
               "Small Straight(30)", "Large Straight(40)",
               "Yahtzee(50)","Chance","Lower Scores", "Total"]

    @staticmethod
    def getConfigs():       # 정적 메소드 : 객체생성 없이 사용 가능
        return Configuration.configs

    # 7 - Upper Scores
    # 8 - Upper Bonus(35)
    # 9 - Three of a kind
    # 10 - Four of a kind
    # 11 - Full House(25)
    # 12 - Small Straight(30)
    # 13 - Large Straight(40)
    # 14 - Yahtzee(50)
    # 15 - Chance
    # 16 - Lower Scores
    # 17 - Total

    @staticmethod
    def score(row, d):
        # row에 따라 주사위 점수를 계산 반환. 예를 들어, row가 0이면 "Ones"가 채점되어야 함.
        # row가 2면, "Threes"가 득점되어야 함.
        # row가 득점(scored)하지 않아야 하는 버튼(즉, UpperScore, UpperBonus, LowerScore, Total 등)
        # 을 나타내는 경우, -1을 반환.
        if 0 <= row < 6:
            return Configuration.scoreUpper(d, row + 1)
        elif row == 8:
            return Configuration.scoreThreeOfAKind(d)
        elif row == 9:
            return Configuration.scoreFourOfAKind(d)
        elif row == 10:
            return Configuration.scoreFullHouse(d)
        elif row == 11:
            return Configuration.scoreSmallStraight(d)
        elif row == 12:
            return Configuration.scoreLargeStraight(d)
        elif row == 13:
            return Configuration.scoreYahtzee(d)
        elif row == 14:
            return Configuration.sumDie(d)

    @staticmethod
    def scoreUpper(d, num):
        # Upper Section 구성(Ones, Twos, Threes, ...)에 대해 주사위 점수를 매김.
        # 예를 들어, num이 1이면 "Ones"구성의 주사위 점수를 반환.
        def Cal(d, num):
            cnt = 0
            for i in range(0, 5):
                if num == d[i].getRoll():
                    cnt += num
            if cnt > 0:
                return cnt
            else:
                return 0

        if num == 1:
            return Cal(d, num)
        elif num == 2:
            return Cal(d, num)
        elif num == 3:
            return Cal(d, num)
        elif num == 4:
            return Cal(d, num)
        elif num == 5:
            return Cal(d, num)
        elif num == 6:
            return Cal(d, num)

    @staticmethod
    def scoreThreeOfAKind(d):
        check = [i for i in range(1, 7)]
        cnt = 0
        for i in range(0, 6):
            for j in range(0, 5):
                if check[i] == d[j].getRoll():
                    cnt += 1
            if cnt >= 3:
                s = [d[k].getRoll() for k in range(0, 5)]
                return sum(s)
            cnt = 0
        return 0

    @staticmethod
    def scoreFourOfAKind(d):
        check = [i for i in range(1, 7)]
        cnt = 0
        for i in range(0, 6):
            for j in range(0, 5):
                if check[i] == d[j].getRoll():
                    cnt += 1
            if cnt >= 4:
                s = [d[k].getRoll() for k in range(0, 5)]
                return sum(s)
            cnt = 0
        return 0

    @staticmethod
    def scoreFullHouse(d):
        check = [i for i in range(1, 7)]
        cnt = [0 for i in range(0, 6)]
        for i in range(0, 6):
            for j in range(0, 5):
                if check[i] == d[j].getRoll():
                    cnt[i] += 1
            if cnt[i] < 2:
                cnt[i] = 0
        if sum(cnt) == 5:
            return 25
        return 0

    @staticmethod
    def scoreSmallStraight(d):
        # 1 2 3 4 or 2 3 4 5 or 3 4 5 6 검사
        # 1 2 2 3 4 or 1 2 3 4 6 or 1 3 4 5 6 or 2 3 4 4 5
        lst = [d[k].getRoll() for k in range(0, 5)]
        lst.sort()
        lst = list(set(lst))
        if len(lst) < 4:
            return 0

        cnt = 0
        for i in range(0, 3):
            for j in range(0, 4):
                if lst[j] == i + j + 1:
                    cnt += 1
            if cnt >= 4:
                return 30
            cnt = 0
        return 0


    @staticmethod
    def scoreLargeStraight(d):
        # 1 2 3 4 5 or 2 3 4 5 6 검사
        lst = [d[k].getRoll() for k in range(0, 5)]
        lst.sort()
        if len(lst) < 5:
            return 0

        cnt = 0
        for i in range(0, 2):
            for j in range(0, 5):
                if lst[j] == i + j + 1:
                    cnt += 1
            if cnt == 5:
                return 40
            cnt = 0
        return 0

    @staticmethod
    def scoreYahtzee(d):
        check = [i for i in range(1, 7)]
        cnt = [0 for i in range(0, 6)]
        for i in range(0, 5):
            for j in range(0, 6):
                if check[j] == d[i].getRoll():
                    cnt[j] += 1

        for i in range(0, 6):
            if cnt[i] == 5:
                return 50
        return 0

    @staticmethod
    def sumDie(d):
        lst = [d[i].getRoll() for i in range(0, 5)]
        return sum(lst)

