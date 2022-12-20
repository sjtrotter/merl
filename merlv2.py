#!/usr/bin/env python

import os
import tkinter as tk
from tkinter import ttk
import shutil as sh
import zipfile as zip
import webbrowser as web
from PIL import ImageTk,Image
# import win32api as win


class Merl(tk.Frame):

    def __init__(self, root):
        tk.Frame.__init__(self)
        self.root = root
        self.root.title("Map Ed")

        self.grid(column=0,row=0,sticky=("nsew"))

        self.rldir_label = ttk.Label(self, justify="right", padding=3, font=('Arial Bold', 9),
            text="RL Location (i.e. C:\\Program Files\\Epic Games\\rocketleague) :")
        self.pillarImg = ImageTk.PhotoImage(Image.open("./images/png/pillars.png"))
        self.pillars_label = ttk.Label(self, image=self.pillarImg)
        self.cosmicImg = ImageTk.PhotoImage(Image.open("./images/png/cosmic.png"))
        self.cosmic_label = ttk.Label(self, image=self.cosmicImg)
        self.doubleImg = ImageTk.PhotoImage(Image.open("./images/png/double.png"))
        self.double_label = ttk.Label(self, image=self.doubleImg)
        self.underpassImg = ImageTk.PhotoImage(Image.open("./images/png/underpass.png"))
        self.underpass_label = ttk.Label(self, image=self.underpassImg)
        self.utopiaImg = ImageTk.PhotoImage(Image.open("./images/png/utopia.png"))
        self.utopia_label = ttk.Label(self, image=self.utopiaImg)
        self.octagonImg = ImageTk.PhotoImage(Image.open("./images/png/octagon.png"))
        self.octagon_label = ttk.Label(self, image=self.octagonImg)
        
        self.RLDir = tk.StringVar()
        self.Pillars = tk.StringVar()
        self.Cosmic = tk.StringVar()
        self.Double = tk.StringVar()
        self.Underpass = tk.StringVar()
        self.Utopia = tk.StringVar()
        self.Octagon = tk.StringVar()

        self.rldir_entry = ttk.Entry(self, width=40, textvariable=self.RLDir)
        self.pillars_entry = ttk.Entry(self, width=30, textvariable=self.Pillars)
        self.cosmic_entry = ttk.Entry(self, width=30, textvariable=self.Cosmic)
        self.double_entry = ttk.Entry(self, width=30, textvariable=self.Double)
        self.underpass_entry = ttk.Entry(self, width=30, textvariable=self.Underpass)
        self.utopia_entry = ttk.Entry(self, width=30, textvariable=self.Utopia)
        self.octagon_entry = ttk.Entry(self, width=30, textvariable=self.Octagon)

        self.rldir_browse = ttk.Button(self, width=10, text="Browse", padding=3, command=lambda: self.browseFiles(self.RLDir))
        self.pillars_browse = ttk.Button(self, text="Browse", padding=3, command=lambda: self.browseFiles(self.RLDir))
        self.cosmic_browse = ttk.Button(self, text="Browse", padding=3, command=lambda: self.browseFiles(self.RLDir))
        self.double_browse = ttk.Button(self, text="Browse", padding=3, command=lambda: self.browseFiles(self.RLDir))
        self.underpass_browse = ttk.Button(self, text="Browse", padding=3, command=lambda: self.browseFiles(self.RLDir))
        self.utopia_browse = ttk.Button(self, text="Browse", padding=3, command=lambda: self.browseFiles(self.RLDir))
        self.octagon_browse = ttk.Button(self, text="Browse", padding=3, command=lambda: self.browseFiles(self.RLDir))
        self.clear_settings = ttk.Button(self, text="Clear Maps", padding=5, command=self.clearSettings)
        self.save_settings = ttk.Button(self, text="Save & Apply", padding=5, command=self.saveSettings)

        self.steam_link = ttk.Label(self, justify="center", text="Steam Workshop Maps",font=('Helveticabold', 12), foreground="blue", cursor="hand2")
        self.steam_dl_link = ttk.Label(self, justify="center", text="Steam Workshop Downloader",font=('Helveticabold', 12), foreground="blue", cursor="hand2")

        self.steam_link.bind("<Button-1>", lambda e: web.open_new_tab("https://steamcommunity.com/app/252950/workshop/"))
        self.steam_dl_link.bind("<Button-1>", lambda e: web.open_new_tab("https://steamworkshopdownloader.io/"))

        self.steam_link.grid(column=0, row=0, columnspan=2, sticky=(tk.N,tk.E,tk.S,tk.W))
        self.steam_dl_link.grid(column=2, row=0, columnspan=2, sticky=(tk.N,tk.S,tk.E,tk.W))
        self.rldir_label.grid(column=0, row=1, columnspan=2, sticky=(tk.E))
        self.rldir_entry.grid(column=2, row=1, columnspan=1, sticky=(tk.N,tk.S,tk.W,tk.E))
        self.rldir_browse.grid(column=3, row=1, sticky=(tk.W,tk.E))
        self.pillars_label.grid(column=0, row=2, columnspan=2, sticky=(tk.N,tk.W,tk.E,tk.S))
        self.cosmic_label.grid(column=2, row=2, columnspan=2, sticky=(tk.N,tk.W,tk.E,tk.S))
        self.pillars_entry.grid(column=0, row=3, sticky=(tk.W,tk.E,tk.N,tk.S))
        self.pillars_browse.grid(column=1, row=3, sticky=(tk.W,tk.E))
        self.cosmic_entry.grid(column=2, row=3, sticky=(tk.W,tk.E,tk.N,tk.S))
        self.cosmic_browse.grid(column=3, row=3, sticky=(tk.W,tk.E))
        self.double_label.grid(column=0, row=4, columnspan=2, sticky=(tk.N,tk.W,tk.E,tk.S))
        self.underpass_label.grid(column=2, row=4, columnspan=2, sticky=(tk.N,tk.W,tk.E,tk.S))
        self.double_entry.grid(column=0,row=5,sticky=(tk.W,tk.E,tk.N,tk.S))
        self.double_browse.grid(column=1, row=5, sticky=(tk.W,tk.E))
        self.underpass_entry.grid(column=2,row=5,sticky=(tk.W,tk.E,tk.S,tk.N))
        self.underpass_browse.grid(column=3, row=5, sticky=(tk.W,tk.E))
        self.utopia_label.grid(column=0, row=6, columnspan=2, sticky=(tk.N,tk.W,tk.E,tk.S))
        self.octagon_label.grid(column=2,row=6, columnspan=2, sticky=(tk.N,tk.W,tk.E,tk.S))
        self.utopia_entry.grid(column=0, row=7, sticky=(tk.W,tk.E,tk.S,tk.N))
        self.utopia_browse.grid(column=1, row=7, sticky=(tk.W,tk.E))
        self.octagon_entry.grid(column=2, row=7, sticky=(tk.W,tk.E,tk.S,tk.N))
        self.octagon_browse.grid(column=3, row=7, sticky=(tk.W,tk.E))
        self.clear_settings.grid(column=0, row=8, columnspan=2, sticky=(tk.E,tk.W))
        self.save_settings.grid(column=2, row=8, columnspan=2, sticky=(tk.E,tk.W))

    def browseFiles(self, stringVar):
        pass

    def saveSettings(self):
        pass

    def clearSettings(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    merl = Merl(root)
    root.mainloop()