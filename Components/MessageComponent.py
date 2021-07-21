from tkinter import *

class WhiteMessage(Message):
    def __init__(self,parent,text,**kwargs):
        super().__init__(parent, text=text, width=600, font=("Roman",18,"bold"), bg="white", relief=SOLID, borderwidth=2)
        self.configure(**kwargs)