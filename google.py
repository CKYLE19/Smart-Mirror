import os
import tkinter
from PIL import ImageTk, Image

class Google(tkinter.Frame):
    def __init__(self, master:tkinter.Frame=None):
        super().__init__(master, background='green')
        self.grid(row=0, column=1, sticky='nsew')
        img_path = '{cur_dir}/assets/{img}'.format(
            cur_dir=os.path.dirname(os.path.realpath(__file__)),
            img="google_assistant.gif"
        )
        self.frames = [ImageTk.PhotoImage(file=img_path, format='gif -index {}'.format(i)) for i in range(75)]
        self.counter = 0
        self.icon = tkinter.Label(self, height=master.winfo_height(), width=master.winfo_width())
        self.icon.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES)
        self.show_assistant()
        
    def show_assistant(self):
        #print(self.counter)
        self.icon.config(image=self.frames[self.counter])
        self.counter += 1
        if self.counter == 75:
            self.counter = 0
        self.after(100, self.show_assistant)
