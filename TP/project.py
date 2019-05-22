from tkinter import *
from tkinter import font
from tkinter import messagebox

class MountainSearch:
    def __init__(self):
        self.InitTitle()

    def InitTitle(self):
        self.Twindow = Tk()
        self.Twindow.title("검색")
        self.Twindow.geometry("500x300+700+250")
        self.Tcanvas = Canvas(self.Twindow, width=500, height=300, relief="solid", bd=1)
        self.image = PhotoImage(file="mountain.gif")
        self.Tcanvas.create_image(250, 150, image=self.image)
        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')

        Button(self.Twindow, text="검색",
               font=self.TempFont, command=self.nextWindow).place(x=275, y=150)
        self.Tcanvas.pack()
        self.Twindow.mainloop()

    def nextWindow(self):           # 검색 버튼 누르면 실행되는 함수
        self.Twindow.destroy()   # 기존에 있던 타이틀 윈도우 파괴
        self.initResult()        # 결과창 생성

    def initResult(self):        # 결과창 생성
        self.window = Tk()
        self.window.title("검색 결과")
        self.window.geometry("400x402+700+100")
        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')
        self.window.mainloop()


MountainSearch()
