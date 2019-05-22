from tkinter import *



def pressed(X):

    frames[X].tkraise()

window = Tk()
window.geometry("500x300+700+250")
window.title("Mountain Search")
frame0 = Frame(window)
frame0.grid(row=0, column=0)
frames = []

for i in range (3):
    Button(frame0,text="Frame"+str(i),command=lambda X=i: pressed(X)).pack(side=LEFT)
    frames.append(Frame(window))
    frames[i].grid(row=1,column=0)
    label = Label(frames[i],text="FRAME"+str(i),width=10,height=10)
    label.pack()



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
