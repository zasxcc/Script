# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import font
from tkinter import messagebox

import http.client
from xml.dom.minidom import parse, parseString
import Gmail



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
               font=self.TempFont, command=self.nextWindow).place(x=295, y=150)
        self.e = Entry(self.Twindow, font=self.TempFont)
        self.e.place(x=150, y=150, width=140, height=40)

        self.Tcanvas.pack()
        self.Twindow.mainloop()

    def nextWindow(self):           # 검색 버튼 누르면 실행되는 함수
        self.MountainName = self.e.get()        # 타이틀에서 산 이름 받아옴

        conn = http.client.HTTPSConnection("openapi.forest.go.kr")
        url = "openapi/service/trailInfoService/getforeststoryservice?serviceKey=cuVGydw6yzwC%2B6YdfYKOPzXxvC45arm%2F1M1dpN31ZrgomqlojiWkwCq0jZqneeAvoEZxOqR8WrymypQQvq4hpg%3D%3D&mntnNm=%EC%A7%80%EB%A6%AC%EC%82%B0"

        conn.request("GET", url)
        req = conn.getresponse()
        print(req.status,req.reason)
        print(req.read().decode('utf-8'))


        self.Twindow.destroy()   # 기존에 있던 타이틀 윈도우 파괴
        self.initResult()        # 결과창 생성

    def initResult(self):        # 결과창 생성
        self.window = Tk()
        self.window.title("검색 결과")
        self.window.geometry("400x402+700+100")
        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')

        Label(self.window, text=self.MountainName).place(x=0, y=0)

        Button(self.window, text="상세정보", width=10, command=self.B).place(x=0, y=30)
        Button(self.window, text="소재지", width=10, command=self.B).place(x=0, y=60)
        Button(self.window, text="대중교통정보", width=10, command=self.B).place(x=0, y=90)
        Button(self.window, text="주변관광정보", width=10, command=self.B).place(x=0, y=120)
        Button(self.window, text="산행포인트", width=10, command=self.B).place(x=0, y=150)
        Button(self.window, text="100대명산", width=10, command=self.B).place(x=0, y=180)
        Button(self.window, text="E-Mail 보내기", width=10, command=Gmail.sendMail).place(x=0, y=210)

        scroll = Scrollbar(self.window)
        text = Text(self.window, width=41, height=30, borderwidth=5, relief="ridge", yscrollcommand=scroll.set)
        scroll.place(x=380, y=0, height=402)
        text.place(x=80, y=0)

        self.window.mainloop()

    def B(self):
        pass


MountainSearch()
