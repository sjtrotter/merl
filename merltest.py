#!/usr/bin/env python

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
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
        x = 0
        y = 2
        for map in ["pillars","cosmic","double","underpass","utopia","octagon"]:
            self.widgets[map+"-image"] = ImageTk.PhotoImage(Image.open("./images/png/"+map+".png"))
            self.widgets[map+"-label"] = ttk.Label(self, image=self.widgets[map+"-image"])
            self.widgets[map+"-string"]= tk.StringVar()
            self.widgets[map+"-entry"] = ttk.Entry(self, textvariable=self.widgets[map+"-string"])
            self.widgets[map+"-button"]= ttk.Button(self, text="Browse", padding=3, command=lambda: self.browseFiles(self.widgets[map+"-string"]))
            self.widgets[map+"-label"].grid(column=x, row=y, columnspan=2)
            self.widgets[map+"-entry"].grid(column=x, row=y+1, sticky="we", padx=3, pady=0)
            self.widgets[map+"-button"].grid(column=x+1, row=y+1, sticky="we")
            x += 2
            if x > 2:
                x = 0
                y += 2

        self.widgets["cosmic-string"].set("/home/betty/test.upk")
        print(self.widgets)
            

        

    def browseFiles(self, stringVar):
        print(stringVar.get())
        filename = fd.askopenfilename(  initialdir=os.path.split(stringVar.get()), \
                                        title="Select Map", \
                                        filetypes=(("Map Files", "*.upk *.udk"),
                                                    ("ZIP Files", "*.zip")))
        if filename != "":
            stringVar.set(filename)
            return filename



root = tk.Tk()
merl = Merl(root)
root.mainloop()