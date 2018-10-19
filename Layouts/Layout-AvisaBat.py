from tkinter import *

master = Tk()
from tkinter import filedialog

master.geometry('330x150')
master.title("Regista hora de n disturbe")

def callback():
    print e.get()
    print i.get()
    Save()

def Save():
    name = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    name.write(e.get())
    name.write(i.get())



label_2 = Label(master, text="Hora de Inicio: ",width=20,font=("bold", 9))
label_2.place(x=0,y=30)

e = Entry(master)
e.pack()

e.focus_set()
e.place(x=130,y=30)

label_3 = Label(master, text="Hora do fim: ",width=20,font=("bold", 9))
label_3.place(x=5,y=60)

i = Entry(master)
i.pack()
i.focus_set()
i.place(x=130,y=60)


b = Button(master, text="Gravar", width=60,bg='brown',fg='white', command=callback)
b.pack()

mainloop()



