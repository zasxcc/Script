from tkinter import *
from tkinter import font
from tkinter import messagebox
from player import *
from dice import *
from configuration import *


class YahtzeeBoard:
    UPPERTOTAL = 6      # UpperScore 범주 인덱스
    UPPERBONUS = 7      # UpperBonus 범주 인덱스
    LOWERTOTAL = 15     # LowerScore 범주 인덱스
    TOTAL = 16          # Total      범주 인덱스
    dice = []           # Dice 객체 리스트
    diceButtons = []    # diceButton 리스트
    fields = []         # 각 플레이어 점수판 2차원 리스트
                        # 열 플레이어, 0열=플레이어1, 1열=플레이어2, ...
                        # 17행 점수 = 카테고리 13행 + upperScore + upperBonus + LowerScore + Total
    players = []        # player 객체 리스트
    numPlayers = 0
    player = 0          # 플레이어 순서를 제어
    round = 0           # 13라운드를 제어
    roll = -1            # 각 라운드마다 3번 굴리기 roll을 할 수 있음.

    def __init__(self):
        self.InitPlayers()

    def InitPlayers(self):
        self.pwindow = Tk()
        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')
        self.label = []
        self.entry = []
        self.label.append(Label(self.pwindow, text="플레이어  명수", font=self.TempFont))
        self.label[0].grid(row=0, column=0)

        for i in range(1, 11):
            self.label.append((Label(self.pwindow, text="플레이어" + str(i) + " 이름", font=self.TempFont)))
            self.label[i].grid(row=i, column=0)

        for i in range(11):
            self.entry.append(Entry(self.pwindow, font=self.TempFont))
            self.entry[i].grid(row=i, column=1)

        Button(self.pwindow, text="Yahtzee 플레이어 설정 완료",
               font=self.TempFont, command=self.playerNames).grid(row=11, column=0)
        self.pwindow.mainloop()

    def playerNames(self):          # 플레이어 설정 완료 버튼 누르면 실행되는 함수
        self.numPlayers = int(self.entry[0].get())
        for i in range(1, self.numPlayers + 1):
            self.players.append(Player(str(self.entry[i].get())))
        self.pwindow.destroy()
        self.initInterface()        # Yahtzee 보드판 플레이어 명수 만큼 생성

    def initInterface(self):        # Yahtzee 보드 윈도우 생성
        self.window = Tk("Yahtzee Game")
        self.window.geometry("1000x800")
        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')

        for i in range(5):      # Dice 객체 5개 생성
            self.dice.append(Dice())

        self.rollDice = Button(self.window, text="Roll Dice",
                               font=self.TempFont, command=self.rollDiceListener)    # Roll Dice 버튼
        self.rollDice.grid(row=0, column=0)

        for i in range(5):  # Dice 버튼 5개 생성
            self.diceButtons.append(Button(self.window, text="?", font=self.TempFont,
                                           width=8, command=lambda row=i: self.diceListener(row)))
            # 각각의 dice 버튼에 대한 이벤트 처리 diceListener 연결
            # 람다 함수를 이용해 diceListener 매개변수 설정하면 하나의 Listener로 해결
            self.diceButtons[i]['state'] = 'disabled'
            self.diceButtons[i]['bg'] = 'light gray'
            self.diceButtons[i].grid(row=i + 1, column=0)

        for i in range(self.TOTAL + 2):     # i행 : 점수
            Label(self.window, text=Configuration.configs[i], font=self.TempFont).grid(row=i, column=1)
            for j in range(self.numPlayers):       # j열 : 플레이어
                if i == 0:      # 플레이어 이름 표시
                    Label(self.window, text=self.players[j].toString(),
                          font=self.TempFont).grid(row=i, column=2 + j)
                else:
                    if j == 0:      # 각 행마다 한번씩 리스트 추가, 다중 플레이어 지원
                        self.fields.append(list())

                    # i - 1 행에 플레이어 개수 만큼 버튼 추가하고 이벤트 Listener 설정, 매개변수 설정
                    self.fields[i - 1].append(Button(self.window, text="", font=self.TempFont,
                                                     width=8, command=lambda row=i-1: self.categoryListener(row)))
                    self.fields[i - 1][j].grid(row=i, column=2 + j)
                    # 누를 필요 없는 버튼은 disable 시킴
                    if j != self.player or i - 1 == self.UPPERTOTAL or i - 1 == self.UPPERBONUS \
                        or i - 1 == self.LOWERTOTAL or i - 1 == self.TOTAL:
                        self.fields[i - 1][j]['state'] = 'disabled'
                        self.fields[i - 1][j]['bg'] = 'light gray'
        # 상태 메시지 출력
        self.bottomLabel = Label(self.window, text=self.players[self.player].toString() +
                                                   "차례 : Roll Dice 버튼을 누르세요", width=35, font=self.TempFont)
        self.bottomLabel.grid(row=self.TOTAL + 2, column=0)
        self.window.mainloop()

    def rollDiceListener(self):
        if self.roll == -1:
            self.roll += 1
            for i in range(5):
                self.diceButtons[i]['state'] = 'normal'
                self.diceButtons[i]['bg'] = 'gray93'
        for i in range(5):
            if self.diceButtons[i]['state'] != 'disabled':
                self.dice[i].rollDie()
                self.diceButtons[i].configure(text=str(self.dice[i].getRoll()))

        if self.roll == 0 or self.roll == 1:
            self.roll += 1
            self.rollDice.configure(text="Roll Again")
            self.bottomLabel.configure(text="보관할 주사위 선택 후 Roll Again")
        elif self.roll == 2:
            self.bottomLabel.configure(text="카테고리를 선택하세요")
            self.rollDice['state'] = 'disabled'
            self.rollDice['bg'] = 'light gray'

    def diceListener(self, row):
        self.diceButtons[row]['state'] = 'disabled'
        self.diceButtons[row]['bg'] = 'light gray'

    def categoryListener(self, row):
        score = Configuration.score(row, self.dice)     # 점수 계산
        index = row
        if row > 7:
            index = row - 2

        # 선택한 카테고리 점수 적고 disable 시킴
        self.players[self.player].setScore(score, index)
        self.players[self.player].setAtUsed(index)
        self.fields[row][self.player].configure(text=str(score))
        self.fields[row][self.player]['state'] = 'disable'
        self.fields[row][self.player]['bg'] = 'light gray'

        # UPPER category가 전부 사용되었으면 UpperScore, UpperBonus 계산
        if self.players[self.player].allUpperUsed():
            self.fields[self.UPPERTOTAL][self.player].configure(text=str(self.players[self.player].getUpperScore()))
            if self.players[self.player].getUpperScore() >= 63:
                self.fields[self.UPPERBONUS][self.player].configure(text="35")  # UPPERBONUS = 7
            else:
                self.fields[self.UPPERBONUS][self.player].configure(text="0")  # UPPERBONUS = 7

        # LOWER category 전부 사용되었으면 LowerScore 계산
        if self.players[self.player].allLowerUsed():
            self.fields[self.LOWERTOTAL][self.player].configure(text=str(self.players[self.player].getLowerScore()))

        # UPPER category와 LOWER category가 전부 사용되었으면 TOTAL 계산
        if self.players[self.player].allUpperUsed() and self.players[self.player].allLowerUsed():
            self.fields[self.TOTAL][self.player].configure(text=\
                        str(self.players[self.player].getUpperScore() + self.players[self.player].getLowerScore()))

        # 다음 플레이어로 넘어가고 선택할 수 없는 카테고리들은 disable 시킴
        self.palyer = (self.player + 1) % self.numPlayers
        for i in range(self.TOTAL + 1):
            for j in range(self.numPlayers):
                self.fields[i - 1][j]['state'] = 'disabled'
                self.fields[i - 1][j]['bg'] = 'light gray'

        # 라운드 증가 시키고 종료 검사
        #if self.player == 0:
        #    self.round += 1
        if self.round == 12 and self.player == self.numPlayers - 1:
            ts = [0 for i in range(0, self.numPlayers)]
            for i in range(0, self.numPlayers):
                ts[i] += self.players[i].getUpperScore() + self.players[i].getLowerScore()
            s = "승자 : " + self.players[ts.index(max(ts))].toString() + "\n" + str(max(ts)) + "점으로 승리!"
            messagebox.showinfo("게임 종료", s)
            self.bottomLabel.configure(text="게임 종료")
            self.fields[self.TOTAL - 1][0]['state'] = 'disabled'
            self.fields[self.TOTAL - 1][0]['bg'] = 'light gray'
            self.rollDice['state'] = 'disabled'
            self.rollDice['bg'] = 'light gray'
            for i in range(5):
                self.diceButtons[i]['state'] = 'disabled'
                self.diceButtons[i]['bg'] = 'light gray'
            return 0
        
        # 다시 Roll Dice와 diceButtons 버튼 활성화, bottomLabel 초기화
        for i in range(5):
            self.diceButtons[i]['state'] = 'normal'
            self.diceButtons[i]['bg'] = 'gray93'
            self.dice[i].rollDie()
            self.diceButtons[i].configure(text=str(self.dice[i].getRoll()))

        for i in range(self.TOTAL + 1):     # 6, 7, 15, 16
            if i - 1 != self.UPPERTOTAL and i - 1 != self.UPPERBONUS \
                    and i - 1 != self.LOWERTOTAL and i - 1 != self.TOTAL:
                self.fields[i - 1][self.palyer]['state'] = 'normal'
                self.fields[i - 1][self.palyer]['bg'] = 'gray93'

        for j in range(0, self.numPlayers):
            for i in range(0, 14):
                if i < 6:
                    if self.players[j].getUsed(i):
                        self.fields[i][j]['state'] = 'disabled'
                        self.fields[i][j]['bg'] = 'light gray'
                if i >= 8:
                    if self.players[j].getUsed(i - 2):
                        self.fields[i][j]['state'] = 'disabled'
                        self.fields[i][j]['bg'] = 'light gray'

        self.player += 1
        self.roll = -1
        self.rollDice['state'] = 'normal'
        self.rollDice['bg'] = 'gray93'
        if self.player == self.numPlayers:
            self.player = 0
            self.round += 1
        self.bottomLabel.configure(text=self.players[self.player].toString() + "차례 : Roll Dice 버튼을 누르세요")
        self.rollDice.configure(text="Roll Dice")
        for i in range(5):
            self.diceButtons[i]['state'] = 'disabled'
            self.diceButtons[i]['bg'] = 'light gray'
            self.diceButtons[i].configure(text="?")


YahtzeeBoard()
