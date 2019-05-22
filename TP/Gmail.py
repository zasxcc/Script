# -*- coding: utf-8 -*-
import mimetypes
import mysmtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

#global value
def sendMail():
    host = "smtp.gmail.com" # Gmail STMP 서버 주소.
    port = "587"
    htmlFileName = "logo.html"

    senderAddr = "zasxcc@gmail.com"     # 보내는 사람 email 주소.
    recipientAddr = "zasxcc@naver.com"   # 받는 사람 email 주소.

    msg = MIMEBase("multipart", "alternative")
    msg['Subject'] = "Test email in Python 3.0"
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    # MIME 문서를 생성합니다.
    htmlFD = open(htmlFileName, 'rb')
    HtmlPart = MIMEText(htmlFD.read(),'html', _charset = 'UTF-8' )
    htmlFD.close()

    # 만들었던 mime을 MIMEBase에 첨부 시킨다.
    msg.attach(HtmlPart)

    path = r'C:\Users\Park\Desktop\SCRIPT\chapter25.pptx'
    part = MIMEBase("application", "octet-stream")
    part.set_payload(open(path, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"'%os.path.basename(path))

    msg.attach(part)

    # 메일을 발송한다.
    s = mysmtplib.MySMTP(host,port)
    #s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("zasxcc@@gmail.com","dlsgur932!")
    s.sendmail(senderAddr , [recipientAddr], msg.as_string())
    s.close()