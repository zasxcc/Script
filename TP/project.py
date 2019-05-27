# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import font
from tkinter import messagebox

import http.client
from xml.etree import ElementTree
import urllib.parse
import urllib.request
import Gmail


class MountainSearch:
    def __init__(self):
        self.InitTitle()

    def InitTitle(self):       # 타이틀 윈도우
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
        self.MountainName = self.e.get()       # 타이틀에서 산 이름 받아옴
        self.mntnnm = urllib.parse.quote(self.e.get())

        conn = http.client.HTTPConnection("openapi.forest.go.kr")
        url = "http://openapi.forest.go.kr/openapi/service/trailInfoService/getforeststoryservice"
        url += "?serviceKey=cuVGydw6yzwC%2B6YdfYKOPzXxvC45arm%2F1M1dpN31ZrgomqlojiWkwCq0jZqneeAvoEZxOqR8WrymypQQvq4hpg%3D%3D"
        url += "&mntnNm="
        url += self.mntnnm

        conn.request("GET", url)
        req = conn.getresponse()
        self.tree = ElementTree.fromstring(req.read().decode('utf-8'))

        self.Twindow.destroy()   # 기존에 있던 타이틀 윈도우 파괴
        self.InitResult()        # 결과창 생성

    def InitResult(self):        # 결과창 생성
        self.window = Tk()
        self.window.title("검색 결과")
        self.window.geometry("400x402+700+100")
        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')

        Label(self.window, text=self.MountainName).place(x=0, y=0)

        Button(self.window, text="상세정보", width=10, command=self.Information).place(x=0, y=30)
        Button(self.window, text="소재지", width=10, command=self.Address).place(x=0, y=60)
        Button(self.window, text="대중교통정보", width=10, command=self.PublicTransportInfo).place(x=0, y=90)
        Button(self.window, text="주변관광정보", width=10, command=self.TourismInfo).place(x=0, y=120)
        Button(self.window, text="산행포인트", width=10, command=self.HikingPoint).place(x=0, y=150)
        Button(self.window, text="100대명산", width=10, command=self.SpecialMountain).place(x=0, y=180)
        Button(self.window, text="개관", width=10, command=self.Survey).place(x=0, y=210)
        Button(self.window, text="E-Mail 보내기", width=10, command=Gmail.sendMail).place(x=0, y=240)
        Button(self.window, text="지도", width=10, command=self.B).place(x=0, y=270)
        Button(self.window, text="텔레그램 봇", width=10, command=self.B).place(x=0, y=300)
        Button(self.window, text="재검색", width=10, command=self.reSearch).place(x=0, y=330)

        scroll = Scrollbar(self.window)
        self.text = Text(self.window, width=41, height=30, borderwidth=5, relief="ridge", yscrollcommand=scroll.set)
        scroll.place(x=380, y=0, height=402)
        self.text.place(x=80, y=0)

        self.window.mainloop()

    def B(self):
        pass

    def reSearch(self):
        self.window.destroy()
        self.InitTitle()

    def Information(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.MountainInfo = item.find("mntninfodtlinfocont")

            self.MountainInfo.text = self.MountainInfo.text.replace('<BR>', '\n')
            self.MountainInfo.text = self.MountainInfo.text.replace('br /', '\n')
            self.MountainInfo.text = self.MountainInfo.text.replace('&lt;', '\n')
            self.MountainInfo.text = self.MountainInfo.text.replace('&gt;', '\n')
            self.MountainInfo.text = self.MountainInfo.text.replace('&amp;', '\n')
            self.MountainInfo.text = self.MountainInfo.text.replace('nbsp;', '\n')

            self.text.insert(1.0, self.MountainInfo.text)
            self.height = item.find("mntninfohght")
            self.sub_name = item.find("mntnsbttlinfo")
            self.name = item.find("mntnnm")

        self.text.insert(1.0, "높이 : " + self.height.text + '\n\n')
        self.text.insert(1.0, "산의 부제 : " + self.sub_name.text + '\n\n')
        self.text.insert(1.0, self.name.text + '\n\n')

        print(self.text.get(1.0, END))      # 텍스트 받기

    def Address(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.MountainAddress = item.find("mntninfopoflc")
            self.text.insert(1.0, self.MountainAddress.text + '\n')

    def PublicTransportInfo(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.PTInfo = item.find("pbtrninfodscrt")
            self.PTInfo.text = self.PTInfo.text.replace('<BR>', '\n')
            self.PTInfo.text = self.PTInfo.text.replace('br /', '\n')
            self.PTInfo.text = self.PTInfo.text.replace('&lt;', '\n')
            self.PTInfo.text = self.PTInfo.text.replace('&gt;', '\n')
            self.PTInfo.text = self.PTInfo.text.replace('&amp;', '\n')
            self.PTInfo.text = self.PTInfo.text.replace('nbsp;', '\n')
            self.text.insert(1.0, self.PTInfo.text)

            self.PTInfo2 = item.find("ptmntrcmmncoursdscrt")
            self.PTInfo2.text = self.PTInfo2.text.replace('<BR>', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('br /', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('&lt;', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('&amp;', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('nbsp;', '\n')
            self.text.insert(1.0, self.PTInfo2.text)

    def TourismInfo(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.TourInfo = item.find("crcmrsghtnginfodscrt")
            self.TourInfo.text = self.TourInfo.text.replace('<BR>', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('br /', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('&lt;', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('&gt;', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('&amp;', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('nbsp;', '\n')
            self.text.insert(1.0, self.TourInfo.text)

    def HikingPoint(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.HP = item.find("hkngpntdscrt")
            self.HP.text = self.HP.text.replace('<BR>', '\n')
            self.HP.text = self.HP.text.replace('br /', '\n')
            self.HP.text = self.HP.text.replace('&lt;', '\n')
            self.HP.text = self.HP.text.replace('&gt;', '\n')
            self.HP.text = self.HP.text.replace('&amp;', '\n')
            self.HP.text = self.HP.text.replace('nbsp;', '\n')
            self.text.insert(1.0, self.HP.text)

    def SpecialMountain(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.SM = item.find("hndfmsmtnslctnrson")
            self.SM.text = self.SM.text.replace('<BR>', '\n')
            self.SM.text = self.SM.text.replace('br /', '\n')
            self.SM.text = self.SM.text.replace('&lt;', '\n')
            self.SM.text = self.SM.text.replace('&gt;', '\n')
            self.SM.text = self.SM.text.replace('&amp;', '\n')
            self.SM.text = self.SM.text.replace('nbsp;', '\n')
            self.text.insert(1.0, self.SM.text)

    def Survey(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.Survey = item.find("mntninfodscrt")
            self.Survey.text = self.Survey.text.replace('<BR>', '\n')
            self.Survey.text = self.Survey.text.replace('br /', '\n')
            self.Survey.text = self.Survey.text.replace('&lt;', '\n')
            self.Survey.text = self.Survey.text.replace('&gt;', '\n')
            self.Survey.text = self.Survey.text.replace('&amp;', '\n')
            self.Survey.text = self.Survey.text.replace('nbsp;', '\n')
            if self.Survey.text == '':
                print("defeaf")
            else:
                self.text.insert(1.0, self.Survey.text)






MountainSearch()
