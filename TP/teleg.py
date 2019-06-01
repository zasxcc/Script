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
import sys
import telegram.ext
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules


my_token = '726303271:AAHtmKdF9PEBV4uNxlY2DVfVuz1fyhuAlug'
TEXT = ""
MAIL = ""
mntname = "한라산"
cnt = 0


class MountainSearch:
    def __init__(self):
        global mntname
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
        self.Information()

    def Information(self):
        self.window = Tk()
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
        print(TEXT)
        # print(type(self.text.get(1.0, END)))


    def Address(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.MountainAddress = item.find("mntninfopoflc")
            self.text.insert(1.0, self.MountainAddress.text + '\n')

    def PublicTransportInfo(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.PTInfo = item.find("pbtrninfodscrt")
            self.L.append(self.PTInfo.text)
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
            self.L.append(self.PTInfo2.text)
            self.PTInfo2.text = self.PTInfo2.text.replace('<BR>', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('br /', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('&lt;', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('&amp;', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('nbsp;', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('<p>&', '\n')
            self.PTInfo2.text = self.PTInfo2.text.replace('</p>', '\n')
            self.text.insert(1.0, self.PTInfo2.text)

        if self.L[0] == '':
            self.text.insert(1.0, "대중 교통 정보가 없습니다.")  # 수정 필요

        self.L.clear()

    def TourismInfo(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.TourInfo = item.find("crcmrsghtnginfodscrt")
            self.L.append(self.TourInfo.text)
            self.TourInfo.text = self.TourInfo.text.replace('<BR>', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('br /', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('&lt;', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('&gt;', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('&amp;', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('nbsp;', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('<p>&', '\n')
            self.TourInfo.text = self.TourInfo.text.replace('</p>', '\n')
            self.text.insert(1.0, self.TourInfo.text)

        if self.L[0] == '':
            self.text.insert(1.0, "주변 관광 정보가 없습니다.")
        self.L.clear()

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



    # help reply function
def get_message(bot, update) :
    global mntname
    mntname = update.message.text

    MountainSearch()

    update.message.reply_text(TEXT)


# help reply function
def help_command(bot, update) :
    update.message.reply_text("무엇을 도와드릴까요?")


updater = Updater(my_token)

message_handler = MessageHandler(Filters.text, get_message)
updater.dispatcher.add_handler(message_handler)

help_handler = CommandHandler('help', help_command)
updater.dispatcher.add_handler(help_handler)

updater.start_polling(timeout=3, clean=True)
updater.idle()
