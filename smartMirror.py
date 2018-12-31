import tkinter
from weather import Weather
from clock import Clock
from google import Google

class Screen:
    def __init__(self):
        self.tk = tkinter.Tk()
        self.tk.configure(background='black')
        self.height = self.tk.winfo_height()
        self.width = self.tk.winfo_width()
        self.topFrame = tkinter.Frame(self.tk, background='black', height=self.height/2, width=self.width)
        self.topFrame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES)
        self.bottomFrame = tkinter.Frame(self.tk, background='blue', height=self.height/2, width=self.width)
        self.bottomFrame.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=tkinter.YES)
        self.weather = Weather(self.topFrame)
        #self.google = Google(self.topFrame)
        self.clock = Clock(self.topFrame)
        self.tk.attributes("-fullscreen", True)
        self.tk.bind('<Escape>', self.exit_app)

    def exit_app(self, event=None):
        self.tk.destroy()

if __name__ == '__main__':
    app = Screen()
    app.tk.mainloop()