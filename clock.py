import tkinter
from tkinter.font import Font
from datetime import datetime
from time import strftime

class Clock(tkinter.Frame):
    def __init__(self, master:tkinter.Frame=None, **kwargs):
        super().__init__(master, background='black', height=master.winfo_height(), width=master.winfo_width()/3)
        self.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=tkinter.YES)
        self.font = Font(family="Avenir LT Std 35 Light", size=45, weight="normal")
        self.date = tkinter.Label(
            self,
            background='black',
            fg='white'
        )
        self.date.configure(font=self.font)
        self.date.place(relx=0.7, rely=0.2, anchor=tkinter.CENTER)
        self.time = tkinter.Label(
            self,
            background='black',
            fg='white'
        )
        self.time.configure(font=self.font)
        self.time.place(relx=0.7, rely=0.4, anchor=tkinter.CENTER)
        self.tick()

    def tick(self):
        self.time.configure(text=strftime(
                "%I:%M %p"
            )
        )
        self.date.configure(text=strftime(
                "%a, %b %d"
            )
        )
        self.after(1000, self.tick)
