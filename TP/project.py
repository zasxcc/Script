# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import font
from tkinter import messagebox

import http.client
from xml.etree import ElementTree
import urllib.parse
import urllib.request

import mimetypes
import mysmtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders
import os



TEXT= ""
MAIL = ""


class MountainSearch:
    def __init__(self):
        self.InitTitle()

    def InitTitle(self):       # 타이틀 윈도우
        self.Twindow = Tk()

        self.f1 = PhotoImage(file="anime01.png")
        self.f2 = PhotoImage(file="anime02.png")
        self.f3 = PhotoImage(file="anime03.png")
        self.f4 = PhotoImage(file="anime04.png")
        self.f5 = PhotoImage(file="anime05.png")
        self.f6 = PhotoImage(file="anime06.png")
        self.n = 0
        self.fn = self.f1

        self.Twindow.title("검색")
        self.Twindow.geometry("480x640+700+100")
        self.Tcanvas = Canvas(self.Twindow, width=480, height=640, relief="solid", bd=1)
        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')

        Button(self.Twindow, text="검색",
               font=self.TempFont, command=self.nextWindow).place(x=295, y=250)
        self.e = Entry(self.Twindow, font=self.TempFont)
        self.e.place(x=150, y=250, width=140, height=40)

        self.Twindow.after(0, self.Animation)

        self.Tcanvas.pack()
        self.Twindow.mainloop()

    def Animation(self):
        if 0 <= self.n < 2:
            self.fn = self.f1
            self.n += 1
        elif 2 <= self.n < 4:
            self.fn = self.f2
            self.n += 1
        elif 4 <= self.n < 6:
            self.fn = self.f3
            self.n += 1
        elif 6 <= self.n < 8:
            self.fn = self.f4
            self.n += 1
        elif 8 <= self.n < 10:
            self.fn = self.f5
            self.n += 1
        elif 10 <= self.n < 12:
            self.fn = self.f6
            self.n += 1
        elif self.n == 12:
            self.n = 0

        self.Tcanvas.create_image(240, 320, image=self.fn)
        self.Twindow.after(120, self.Animation)

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
        self.MapCanvas = Canvas(self.window, width=800, height=402)
        self.MapCanvas.pack()
        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')

        Label(self.window, text=self.MountainName).place(x=20, y=5)

        Button(self.window, text="상세정보", width=10, command=self.Information).place(x=0, y=30)
        Button(self.window, text="소재지", width=10, command=self.Address).place(x=0, y=60)
        Button(self.window, text="대중교통정보", width=10, command=self.PublicTransportInfo).place(x=0, y=90)
        Button(self.window, text="주변관광정보", width=10, command=self.TourismInfo).place(x=0, y=120)
        Button(self.window, text="산행포인트", width=10, command=self.HikingPoint).place(x=0, y=150)
        Button(self.window, text="100대명산", width=10, command=self.SpecialMountain).place(x=0, y=180)
        Button(self.window, text="개관", width=10, command=self.Survey).place(x=0, y=210)
        Button(self.window, text="E-Mail 보내기", width=10, command=self.sendMail).place(x=0, y=240)
        Button(self.window, text="지도", width=10, command=self.Map).place(x=0, y=270)
        Button(self.window, text="텔레그램 봇", width=10, command=self.B).place(x=0, y=300)
        Button(self.window, text="재검색", width=10, command=self.reSearch).place(x=0, y=330)
        Button(self.window, text="산높이 그래프", width=10, command=self.Graph).place(x=0, y=360)

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
        global TEXT
        TEXT = self.text.get(1.0, END)
        print(type(self.text.get(1.0, END)))

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

    def sendMail(self):
        # global value
        global MAIL
        self.Twindow2 = Tk()
        self.Twindow2.title("이메일 주소 입력")
        self.Twindow2.geometry("300x100+700+250")
        self.TempFont2 = font.Font(size=5, weight='bold', family='Consolas')

        Button(self.Twindow2, text="보내기",
               font=self.TempFont2, command=self.mailSend).place(x=120, y=50)

        self.e2 = Entry(self.Twindow2, font=self.TempFont2)
        self.e2.place(x=10, y=10, width=280, height=30)

    def mailSend(self):
        global MAIL
        global TEXT
        MAIL = self.e2.get()
        host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
        port = "587"
        messagebox.showinfo("Loading", "이메일 보내는 중...")

        senderAddr = "zasxcc@gmail.com"  # 보내는 사람 email 주소.
        recipientAddr = MAIL  # 받는 사람 email 주소.

        msg = MIMEMultipart()

        msg['Subject'] = "산 상세정보"
        msg['From'] = senderAddr
        msg['To'] = recipientAddr

        self.Information()      # 상세정보 누르지 않아도 여기서 다시 실행

        #####################
        import requests
        import folium
        import pdfcrowd
        import sys

        self.URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyBFVqFYHLQNOYuSVfkiHCv1GkyfUpnpAIY' \
                   '&sensor=false&language=ko&address={}'.format(self.MountainName)
        self.response = requests.get(self.URL)
        self.data = self.response.json()
        self.lat = self.data['results'][0]['geometry']['location']['lat']
        self.lng = self.data['results'][0]['geometry']['location']['lng']
        self.map_osm = folium.Map(location=[self.lat, self.lng])
        folium.Marker([self.lat, self.lng], popup=self.MountainName).add_to(self.map_osm)
        self.map_osm.save('SearchResultMap.html')
        #####################
        # 이 부분에서 지도 버튼을 누르지 않아도 folium을 이용한 html파일 생성.

        ############################### html file to png file

        try:
            # create the API client instance
            client = pdfcrowd.HtmlToImageClient('JanghoPark', '2abdd903f12f616c4f8d039230ee1bf1')

            # configure the conversion
            client.setOutputFormat('gif')
            client.setScreenshotWidth(400)
            client.setScreenshotHeight(400)

            # run the conversion and write the result to a file
            client.convertFileToFile('SearchResultMap.html', 'Searched_Result_Map.gif')
        except pdfcrowd.Error as why:
            # report the error
            sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))

            # handle the exception here or rethrow and handle it at a higher level
            raise



        ################################


        text = TEXT
        htmlFileName = "Searched_Result_Map.gif"
        ig = 'Searched_Result_Map.gif'

        # MIME 문서를 생성합니다.
        htmlFD = open(htmlFileName, 'rb')
        igFD = open(ig, 'rb')
        HtmlPart = MIMEText(htmlFD.read(),'gif', _charset = 'UTF-8' )
        TextPart = MIMEText(text, 'html', _charset='UTF-8')
        igPart = MIMEImage(igFD.read(), 'gif', _charset='UTF-8')
        htmlFD.close()
        igFD.close()
        # 만들었던 mime을 MIMEBase에 첨부 시킨다.
        msg.attach(HtmlPart)
        msg.attach(TextPart)
        msg.attach(igPart)
        # global e, filname
        # filename = filedialog.askopenfilename(initialdir='path', title='select file', filetypes=(('jpeg file, ','*.jpg'), ('all files', '*.*')))
        # path = r'C:\Users\Park\Desktop\SCRIPT\chapter25.pptx'
        # part = MIMEBase("application", "octet-stream")
        # part.set_payload(open(path, 'rb').read())
        # encoders.encode_base64(part)
        # part.add_header('Content-Disposition', 'attachment; filename="%s"'%os.path.basename(path))

        # msg.attach(part)

        # 메일을 발송한다.
        s = mysmtplib.MySMTP(host, port)
        # s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
        s.ehlo()
        s.starttls()
        s.login("zasxcc@gmail.com", "dlsgur932!")
        s.sendmail(senderAddr, [recipientAddr], msg.as_string())
        s.close()

        messagebox.showinfo("Complete", "이메일 보내기 완료!")

    def Map(self):
        import requests
        import folium
        import pdfcrowd
        import sys

        self.URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyBFVqFYHLQNOYuSVfkiHCv1GkyfUpnpAIY' \
              '&sensor=false&language=ko&address={}'.format(self.MountainName)

        self.response = requests.get(self.URL)

        self.data = self.response.json()

        self.lat = self.data['results'][0]['geometry']['location']['lat']
        self.lng = self.data['results'][0]['geometry']['location']['lng']

        self.map_osm = folium.Map(location=[self.lat, self.lng])
        folium.Marker([self.lat, self.lng], popup=self.MountainName).add_to(self.map_osm)
        self.map_osm.save('SearchResultMap.html')

        self.map_url = 'https://www.google.co.kr/maps/search/' + self.MountainName + '/@' + str(self.lat) + ',' + str(self.lng) + ',12z'

        messagebox.showinfo("알림", "지도 그리는 중...")

        ############################### html file to png file

        try:
            # create the API client instance
            client = pdfcrowd.HtmlToImageClient('JanghoPark', '2abdd903f12f616c4f8d039230ee1bf1')

            # configure the conversion
            client.setOutputFormat('gif')
            client.setScreenshotWidth(400)
            client.setScreenshotHeight(400)

            # run the conversion and write the result to a file
            client.convertFileToFile('SearchResultMap.html', 'Searched_Result_Map.gif')
        except pdfcrowd.Error as why:
            # report the error
            sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))

            # handle the exception here or rethrow and handle it at a higher level
            raise

        ################################
        #import time
        #time.sleep(5)       # 해결된 줄 알았는데 종종 잘려서 그러질 때가 있음

        self.image = PhotoImage(file='Searched_Result_Map.gif')
        self.window.geometry("800x402")
        self.MapCanvas.create_image(600, 201, image=self.image)

        messagebox.showinfo("알림", "지도가 완성되었습니다!")

        Button(self.window, text="구글 지도 연동", overrelief="solid", width=15, command=self.WebViewer).place(x=600, y=350)


        # google map api로 경도 위도 받아와 foliun으로 email 전송을 위한 html 파일 저장.
        # 지도 버튼 누르면 웹뷰 윈도우로 아예 구글 맵 검색되도록 구현.
        # 웹뷰 윈도우가 생성되면 기존 Tk 윈도우가 응답하지 않는 문제가 있음.

    def WebViewer(self):
        import webview
        webview.create_window('Google Map', self.map_url, width=1280, height=720)

    def Graph(self):
        # 그래프 그리는데, 95개 산의 높이 정보를 파싱하기 때문에 시간이 오래 걸림
        self.f = open("100대산(중복제외95).txt", 'r+')
        self.string = ''
        self.string += self.f.read()
        self.MountainList = []
        self.MountainList += self.string.split('\n')
        self.HeightList = []
        self.NameList = []

        conn = http.client.HTTPConnection("openapi.forest.go.kr")
        graph_url = "http://openapi.forest.go.kr/openapi/service/trailInfoService/getforeststoryservice"
        graph_url += "?serviceKey=cuVGydw6yzwC%2B6YdfYKOPzXxvC45arm%2F1M1dpN31ZrgomqlojiWkwCq0jZqneeAvoEZxOqR8WrymypQQvq4hpg%3D%3D"
        graph_url += "&mntnNm="
        url = ''

        messagebox.showinfo("알림", "그래프 그리는 중...")

        for i in range(len(self.MountainList)):
            name = urllib.parse.quote(self.MountainList[i])
            url += graph_url + name
            conn.request("GET", url)
            req = conn.getresponse()
            graph_tree = ElementTree.fromstring(req.read().decode('utf-8'))
            url = ''
            for item in graph_tree.iter("item"):
                try:
                    self.HeightList.append(item.find("mntninfohght").text)
                    self.NameList.append(item.find("mntnnm").text)
                    break
                except ValueError:
                    pass

        self.GraphWindow = Tk()
        self.GraphWindow.title("100대 명산 높이 그래프")
        self.GraphWindow.geometry("1280x680")
        self.GraphCanvas = Canvas(self.GraphWindow, width=1280, height=670)
        scrollbar = Scrollbar(self.GraphWindow, orient="horizontal", command=self.GraphCanvas.xview)
        self.GraphCanvas.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(side="bottom", fill="x")

        interval = 20

        for i in range(0, len(self.HeightList)):
            self.GraphCanvas.create_rectangle(i * 10 + interval, 650, (i + 1) * 10 + interval, 650 - (int(self.HeightList[i]) * 0.3), outline="black", fill="blue")
            self.GraphCanvas.create_text(i * 10 + interval + 5, 660, text=self.NameList[i])
            self.GraphCanvas.create_text(i * 10 + interval + 5, 650 - (int(self.HeightList[i]) * 0.3) - 20, text=self.HeightList[i])
            interval += 50

        self.f.close()
        self.NameList.clear()
        self.HeightList.clear()

        self.GraphCanvas.pack()

        self.GraphWindow.bind("<Configure>", self.on)
        self.GraphWindow.mainloop()

    def on(self, event):
        self.GraphCanvas.configure(scrollregion=self.GraphCanvas.bbox("all"))


MountainSearch()
