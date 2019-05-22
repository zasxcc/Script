from tkinter import *

window = Tk()
window.geometry("400x402+700+100")
window.title("Mountain Search")





def B():
    pass


Label(window, text="지리산").place(x=0, y=0)

Button(window, text="상세정보", width=10, command=B).place(x=0, y=30)
Button(window, text="소재지", width=10, command=B).place(x=0, y=60)
Button(window, text="대중교통정보", width=10, command=B).place(x=0, y=90)
Button(window, text="주변관광정보", width=10, command=B).place(x=0, y=120)
Button(window, text="산행포인트", width=10, command=B).place(x=0, y=150)
Button(window, text="100대명산", width=10, command=B).place(x=0, y=180)
Button(window, text="E-Mail 보내기", width=10, command=B).place(x=0, y=210)








scroll = Scrollbar(window)
text = Text(window, width=41, height=30, borderwidth=5, relief="ridge", yscrollcommand=scroll.set)
scroll.place(x=380, y=0)
text.place(x=80, y=0)

window.mainloop()
