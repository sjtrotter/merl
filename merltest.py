#!/usr/bin/env python

import os
import tkinter as tk
from tkinter import ttk
import shutil as sh
import zipfile as zip
from PIL import ImageTk, Image
# import win32api as win


class Merl(tk.Frame):
    
    def __init__(self, root):
        tk.Frame.__init__(self)
        self.root = root
        self.root.title("Map Editor for Rocket League")

        self.grid(column=0,row=0,sticky=("nsew"))

        self.widgets = {}
        # for element in ["image","label","button","entry","stringVar","command"]:
        for map in ["pillars","cosmic","double","underpass","utopia","octagon"]:
            self.widgets[map+"-image"] = ImageTk.PhotoImage(Image.open("./images/png/"+map+".png"))
            self.widgets[map+"-label"] = ttk.Label(self, image=self.widgets[map+"-image"])
            self.widgets[map+"-string"]= tk.StringVar()
            self.widgets[map+"-entry"] = ttk.Entry(self, textvariable=self.widgets[map+"-string"])
            self.widgets[map+"-button"]= ttk.Button(self, text="Browse", padding=3, command=lambda: self.browseFiles(self.widgets[map+"-string"]))

        





root = tk.Tk()
merl = Merl(root)
root.mainloop()