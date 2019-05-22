from tkinter import *

window = Tk()
window.geometry("500x300+700+250")
window.title("Mountain Search")
canvas = Canvas(window, width=500, height=300, relief="solid", bd=1)

image = PhotoImage(file="mountain.gif")

canvas.create_image(250, 150, image=image)



e1 = Entry(window)
e1.place(x=210, y=150, width=60)


def B():
    print(e1.get())


Button(window, text="검색", command=B).place(x=275, y=150)


canvas.pack()
window.mainloop()
