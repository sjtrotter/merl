#!/usr/bin/env python
"""
Map Editor for Rocket League (MERL)
===================================
"""
VERSION = "0.10.1"
"""
 [x] Write python Tkinter interface
 [x] Allow UPK/UDK file choosing
 [x] Allow ZIP file choosing
 [ ] Code to reset map settings
 [ ] Code to restore settings from save file
 [ ] Code to save settings
 [ ] Code to backup original maps
 - Code replace logic for UPK/UDK
 - Code replace logic for ZIP file extract
 - Code restore logic if map slot is empty
"""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import shutil as sh
import zipfile as zip
import webbrowser as web
from PIL import ImageTk, Image
# import win32api as win


class Merl(tk.Frame):
    
    def __init__(self, root):
        tk.Frame.__init__(self)
        self.root = root
        self.root.title("Map Editor for Rocket League")

        self.grid(column=0,row=0,sticky=("nsew"))

        self.widgets = {}
        # Rocket League Directory widgets
        self.widgets["rldir-label"] = ttk.Label(self, justify="right", padding=3, font=('Arial Bold', 10),
            text="RL Folder (C:\\Program Files\\Epic Games\\rocketleague):")
        self.widgets["rldir-label"].grid(column=0, row=0, columnspan=2, sticky="nse")
        self.widgets["rldir-string"] = tk.StringVar()
        self.widgets["rldir-entry"] = ttk.Entry(self, textvariable=self.widgets["rldir-string"])
        self.widgets["rldir-entry"].grid(column=2, row=0, sticky="nsew")
        self.widgets["rldir-button"] = ttk.Button(self,text="Browse", padding=3, width=5, \
            command=lambda: self.chooseDirectory(self.widgets["rldir-string"]))
        self.widgets["rldir-button"].grid(column=3, row=0, sticky="nsew")
        # Workshop widgets
        self.workshop_link = ttk.Label(self, justify='center', text="Workshop Maps",font=('Helveticabold', 12), \
            width=15, foreground="blue", cursor="hand2")
        self.workshop_link.bind("<Button-1>", lambda e: web.open_new_tab("http://rocketleaguemaps.us/"))
        self.workshop_link.grid(column=0, row=1, columnspan=4)
        # set initial grid coords for maps
        x = 0
        y = 2
        # create widgets for each map
        for mapfile in ["pillars","cosmic","double","underpass","utopia","octagon"]:
            self.widgets[mapfile+"-image"] = ImageTk.PhotoImage(Image.open("./images/png/"+mapfile+".png"))
            self.widgets[mapfile+"-label"] = ttk.Label(self, image=self.widgets[mapfile+"-image"])
            self.widgets[mapfile+"-string"]= tk.StringVar()
            self.widgets[mapfile+"-entry"] = ttk.Entry(self, textvariable=self.widgets[mapfile+"-string"])
            self.widgets[mapfile+"-button"]= ttk.Button(self, text="Browse", padding=3, width=5, \
                command=lambda mapfile=mapfile: self.browseFiles(self.widgets[mapfile+"-string"]))
            self.widgets[mapfile+"-label"].grid(column=x, row=y, columnspan=2, sticky="nsew")
            self.widgets[mapfile+"-entry"].grid(column=x, row=y+1, sticky="nsew", padx=2, pady=0)
            self.widgets[mapfile+"-button"].grid(column=x+1, row=y+1, sticky="nsew")

            # update grid coords
            x += 2
            if x > 2:
                x = 0
                y += 2


    def browseFiles(self, stringVar):
        filename = fd.askopenfilename(  initialdir=os.path.split(stringVar.get())[0], \
                                        title="Select Map", \
                                        filetypes=(("Map Files", "*.upk *.udk"),
                                                    ("ZIP Files", "*.zip")))
        if filename != "":
            stringVar.set(filename)
            return filename


    def chooseDirectory(self, stringVar):
        dirname = fd.askdirectory( initialdir=os.path.split(stringVar.get()),
                                        title="Rocket League Directory")
        if dirname != "":
            stringVar.set(dirname)
            return dirname

        return None


root = tk.Tk()
merl = Merl(root)
root.mainloop()