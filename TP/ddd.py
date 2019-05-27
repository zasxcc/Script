from tkinter import*
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk


def Map():
    root = Tk()
    root.geometry("500x500+500+200")

    # openapi로 이미지 url을 가져옴.
    url = "http://tong.visitkorea.or.kr/cms/resource/74/2396274_image2_1.JPG"
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()

    im = Image.open(BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)

    label = Label(root, image=image, height=400, width=400)
    label.pack()
    label.place(x=0, y=0)
    root.mainloop()

