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
        self.topFrame = tkinter.Frame(self.tk, background='black')
        self.topFrame.grid_columnconfigure(0, weight=2)
        self.topFrame.grid_columnconfigure(1, weight=1)
        self.topFrame.grid_columnconfigure(2, weight=3)
        self.topFrame.grid_rowconfigure(0, weight=1)
        self.tk.grid_columnconfigure(0, weight=1)
        self.tk.grid_rowconfigure(0, weight=1)
        self.tk.grid_rowconfigure(1, weight=1)
        self.topFrame.grid(row=0, column=0, sticky='nsew')
        self.bottomFrame = tkinter.Frame(self.tk, background='blue')
        self.bottomFrame.grid(row=1, column=0, sticky='nsew')
        self.weather = Weather(self.topFrame)
        self.google = Google(self.topFrame)
        self.clock = Clock(self.topFrame)
        self.tk.attributes("-fullscreen", True)
        self.tk.bind('<Escape>', self.exit_app)

    def exit_app(self, event=None):
        self.tk.destroy()

if __name__ == '__main__':
    app = Screen()
    app.tk.mainloop()