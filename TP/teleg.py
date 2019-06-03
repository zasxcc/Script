# -*- coding: utf-8 -*-
from tkinter import *


import http.client
from xml.etree import ElementTree
import urllib.parse
import urllib.request

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules


my_token = '726303271:AAHtmKdF9PEBV4uNxlY2DVfVuz1fyhuAlug'
TEXT = ""
MAIL = ""
mntname = ""
mntstr = ""
cnt = 0


class MountainSearch:
    def __init__(self):
        global mntname
        self.window = Tk()
        self.nextWindow(mntname)

    def nextWindow(self, mn):  # 검색 버튼 누르면 실행되는 함수
        self.mntnnm = urllib.parse.quote(mn)
        print(mntname)
        conn = http.client.HTTPConnection("openapi.forest.go.kr")
        url = "http://openapi.forest.go.kr/openapi/service/trailInfoService/getforeststoryservice"
        url += "?serviceKey=cuVGydw6yzwC%2B6YdfYKOPzXxvC45arm%2F1M1dpN31ZrgomqlojiWkwCq0jZqneeAvoEZxOqR8WrymypQQvq4hpg%3D%3D"
        url += "&mntnNm="
        url += self.mntnnm

        conn.request("GET", url)
        req = conn.getresponse()
        self.tree = ElementTree.fromstring(req.read().decode('utf-8'))
        if mntstr == " 상세정보":
            self.Information()
        elif mntstr == " 주소":
            self.Address()
        elif mntstr == " 대중교통":
            self.PublicTransportInfo()
        elif mntstr == " 관광정보":
            self.TourismInfo()

    def Information(self):
        self.text = Text(self.window)
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.MountainInfo = item.find("mntninfodtlinfocont")

            self.MountainInfo.text = self.MountainInfo.text.replace('<BR>', '\n')
            self.MountainInfo.text = self.MountainInfo.text.replace('br /', '\n')
            self.MountainInfo.text = self.MountainInfo.text.replace('&lt;', '\n')
            self.MountainInfo.text = self.MountainInfo.text.replace('&gt;', '\n')
            self.MountainInfo.text = self.MountainInfo.text.replace('&amp;', '\n')
            self.MountainInfo.text = self.MountainInfo.text.replace('nbsp;', '\n')
            self.MountainInfo.text = self.MountainInfo.text.replace('<strong>&', '\n')
            self.MountainInfo.text = self.MountainInfo.text.replace('</strong>', '\n')
            self.MountainInfo.text = self.MountainInfo.text.replace('</p>', '\n')
            self.MountainInfo.text = self.MountainInfo.text.replace('<p>', '\n')

            self.text.insert(1.0, self.MountainInfo.text)
            self.height = item.find("mntninfohght")
            self.sub_name = item.find("mntnsbttlinfo")
            self.name = item.find("mntnnm")

        self.text.insert(1.0, "높이 : " + self.height.text + '\n\n')
        self.text.insert(1.0, "산의 부제 : " + self.sub_name.text + '\n\n')
        self.text.insert(1.0, self.name.text + '\n\n')

        # print(self.text.get(1.0, END))      # 텍스트 받기
        global TEXT
        TEXT = self.text.get(1.0, END)
        #print(TEXT)
        # print(type(self.text.get(1.0, END)))


    def Address(self):
        self.text = Text(self.window)
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.MountainAddress = item.find("mntninfopoflc")
            self.text.insert(1.0, self.MountainAddress.text + '\n')
        global TEXT
        TEXT = self.text.get(1.0, END)

    def PublicTransportInfo(self):
        self.text = Text(self.window)
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.PTInfo = item.find("pbtrninfodscrt")

            self.PTInfo.text = self.PTInfo.text.replace('<BR>', '\n')
            self.PTInfo.text = self.PTInfo.text.replace('br /', '\n')
            self.PTInfo.text = self.PTInfo.text.replace('&lt;', '\n')
            self.PTInfo.text = self.PTInfo.text.replace('&gt;', '\n')
            self.PTInfo.text = self.PTInfo.text.replace('&amp;', '\n')
            self.PTInfo.text = self.PTInfo.text.replace('nbsp;', '\n')
            self.PTInfo.text = self.PTInfo.text.replace('<p>&', '\n')
            self.PTInfo.text = self.PTInfo.text.replace('</p>', '\n')
            self.text.insert(1.0, self.PTInfo.text)

            self.PTInfo2 = item.find("ptmntrcmmncoursdscrt")

            self.PTInfo2.text = self.PTInfo2.text.replace('<BR>', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('br /', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('&lt;', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('&amp;', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('nbsp;', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('<p>&', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('</p>', '\n')
            self.text.insert(1.0, self.PTInfo2.text)

        print(self.text.get(1.0, END))
        global TEXT
        TEXT = self.text.get(1.0, END)


    def TourismInfo(self):
        self.text = Text(self.window)
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.TourInfo = item.find("crcmrsghtnginfodscrt")
            self.TourInfo.text = self.TourInfo.text.replace('<BR>', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('br /', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('&lt;', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('&gt;', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('&amp;', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('nbsp;', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('<p>&', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('</p>', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('&#xD;', '')
            self.text.insert(1.0, self.TourInfo.text)

        global TEXT
        TEXT = self.text.get(1.0, END)


    # help reply function
def get_message(bot, update) :
    global mntname, mntstr
    getMessage = update.message.text
    flag = 0
    mntname = ""
    mntstr = ""
    for item in getMessage:
        if item == " ":
            flag = 1
        if flag == 1:
            mntstr += item
        else:
            mntname += item
    print(mntname)
    if mntstr == " 상세정보":
        MountainSearch()
        update.message.reply_text(TEXT)
    elif mntstr == " 주소":
        MountainSearch()
        update.message.reply_text(TEXT)
    elif mntstr == " 대중교통":
        MountainSearch()
        update.message.reply_text(TEXT)
    elif mntstr == " 관광정보":
        MountainSearch()
        update.message.reply_text(TEXT)
    else:
        update.message.reply_text("머라고 하는지 모르겟어요")





# help reply function
def help_command(bot, update) :
    update.message.reply_text("무엇을 도와드릴까요?")


updater = Updater(my_token)

message_handler = MessageHandler(Filters.text, get_message)
updater.dispatcher.add_handler(message_handler)

help_handler = CommandHandler('help', help_command)
updater.dispatcher.add_handler(help_handler)

updater.start_polling(timeout=5, clean=True)
updater.idle()
