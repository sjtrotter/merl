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
import os,json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import shutil as sh
import zipfile as zip
import webbrowser as web
from PIL import ImageTk, Image
import win32api as win


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
        self.widgets["rldir-label"].grid(column=0, row=0, columnspan=3, sticky="nse")
        self.widgets["rldir-string"] = tk.StringVar()
        self.widgets["rldir-entry"] = ttk.Entry(self, textvariable=self.widgets["rldir-string"], state="disabled")
        self.widgets["rldir-entry"].grid(column=3, row=0, columnspan=2, sticky="nsew")
        self.widgets["rldir-editimage"] = ImageTk.PhotoImage(Image.open("./images/png/edit_button-16.png"))
        self.widgets["rldir-button"] = ttk.Button(self, image=self.widgets["rldir-editimage"], padding=3, width=5, \
            command=lambda: self.chooseDirectory("rldir"))
        self.widgets["rldir-button"].grid(column=5, row=0, sticky="nsew")
        # Workshop link widgets
        self.widgets["workshop-link"] = ttk.Label(self, justify='center', text="Get Workshop Maps",font=('Helveticabold', 12), \
            width=17, foreground="blue", cursor="hand2", padding=3)
        self.widgets["workshop-link"].bind("<Button-1>", lambda e: web.open_new_tab("http://rocketleaguemaps.us/"))
        self.widgets["workshop-link"].grid(column=0, row=1, columnspan=6)
        # set initial grid coords for maps
        x = 0
        y = 2
        # Map widgets
        for mapfile in ["pillars","cosmic","double","underpass","utopia","octagon"]:
            self.widgets[mapfile+"-image"] = ImageTk.PhotoImage(Image.open("./images/png/"+mapfile+".png"))
            self.widgets[mapfile+"-label"] = ttk.Label(self, image=self.widgets[mapfile+"-image"])
            self.widgets[mapfile+"-label"].bind("<Button-1>", lambda e,mapfile=mapfile: self.browseFiles(mapfile))
            self.widgets[mapfile+"-string"]= tk.StringVar()
            self.widgets[mapfile+"-entry"] = ttk.Entry(self, textvariable=self.widgets[mapfile+"-string"], state="disabled")
            self.widgets[mapfile+"-editimage"] = ImageTk.PhotoImage(Image.open("./images/png/edit_button-16.png"))
            self.widgets[mapfile+"-edit"]= ttk.Button(self, image=self.widgets[mapfile+"-editimage"], padding=3, width=5, \
                command=lambda mapfile=mapfile: self.browseFiles(mapfile))
            self.widgets[mapfile+"-clearimage"] = ImageTk.PhotoImage(Image.open("./images/png/trashcan_button-16.png"))
            self.widgets[mapfile+"-clear"]= ttk.Button(self, image=self.widgets[mapfile+"-clearimage"], padding=3, width=5, \
                command=lambda mapfile=mapfile: self.clearFiles(mapfile))
            self.widgets[mapfile+"-label"].grid(column=x, row=y, columnspan=3, sticky="nsew")
            self.widgets[mapfile+"-entry"].grid(column=x, row=y+1, sticky="nsew", padx=2, pady=0)
            self.widgets[mapfile+"-edit"].grid(column=x+1, row=y+1, sticky="nsew")
            self.widgets[mapfile+"-clear"].grid(column=x+2, row=y+1, sticky="nsew")

            # update grid coords
            x += 3
            if x > 3:
                x = 0
                y += 2

        # Clear and Save buttons
        self.widgets["clear-button"] = ttk.Button(self, text="Clear Maps", padding=5, command=self.clearSettings)
        self.widgets["save-button"] = ttk.Button(self, text="Save & Apply", padding=5, command=self.saveSettings)
        self.widgets["clear-button"].grid(column=0, row=8, columnspan=3, sticky="we")
        self.widgets["save-button"].grid(column=3, row=8, columnspan=3, sticky="we")

        # set RLDir relpath to maps
        self.rldir_relpath = "TAGame/CookedPCConsole/"

        if os.path.exists("./maps.merl"):
            self.settings = self.loadSettings()
        else:
            self.settings = self.initializeSettings()

        # set entryboxes to loaded settings
        for setting in self.settings.keys():
            if setting == "rldir-string":
                self.widgets[setting].set(self.settings[setting])
            elif self.settings[setting] == None:
                pass
            else:
                self.widgets[setting].set(os.path.split(self.settings[setting])[1])
        

    def backupMaps(self):
        filenames = ["Labs_CirclePillars_P.upk", "Labs_Cosmic_V4_P.upk", "Labs_Cosmic_P.upk", \
            "Labs_DoubleGoal_V2_P.upk", "Labs_DoubleGoal_P.upk", "Labs_Underpass_P.upk", \
            "Labs_Underpass_v0_p.upk", "Labs_Utopia_P.upk", "Labs_Octagon_02_P.upk","Labs_Octagon_P.upk"]

        for f in filenames:
            fullpath = os.path.join(self.settings['rldir-string'],self.rldir_relpath,f)
            if os.path.exists(fullpath) and not os.path.exists(fullpath+".merl"):
                sh.copyfile(fullpath,fullpath+".merl")


    def verifySettings(self, data):
        verified = True
        if len(data.keys()) != 7:
            verified = False

        for string in data.keys():
            if string not in ["rldir-string", "pillars-string","cosmic-string","double-string","underpass-string","utopia-string","octagon-string"]:
                verified = False
            else: # don't need to verify path if string isnt in the list.
                if not self.verifyPath(data[string]):
                    # instead of reinitializing for one bad path,
                    # just set to none
                    data[string] = None

        if not verified:
            mb.showinfo(title="Corrupted Save", message="Found corrupted save file. Re-initializing.")
            return self.initializeSettings()

        return data


    def loadSettings(self):
        with open("./maps.merl","r") as f:
            data = f.read()

        data = json.loads(data)

        return self.verifySettings(data)


    def initializeSettings(self):
        data = { "rldir-string": "C:\\Program Files\\Epic Games\\rocketleague" }
        for setting in ["pillars","cosmic","double","underpass","utopia","octagon"]:
            data[setting+"-string"] = None
        
        return data


    def verifyPath(self, path):
        if path:
            return os.path.exists(path)
        else:
            return False


    def clearFiles(self, stringVar):
        self.widgets[stringVar+"-string"].set("")
        self.settings[stringVar+"-string"] = None


    def browseFiles(self, stringVar):
        filename = fd.askopenfilename(  initialdir=os.path.split(self.widgets[stringVar+'-string'].get())[0], \
                                        title="Select Map", \
                                        filetypes=(("Map Files", "*.upk *.udk"),
                                                    ("ZIP Files", "*.zip")))

        if filename != "" and self.verifyPath(filename):
            self.widgets[stringVar+'-string'].set(os.path.split(filename)[1])
            self.settings[stringVar+'-string'] = filename
        
        return filename


    def chooseDirectory(self, stringVar):
        dirname = fd.askdirectory( initialdir=os.path.split(self.widgets[stringVar+"-string"].get()),
                                        title="Rocket League Directory")

        if dirname != "" and self.verifyRLPath(dirname):
            self.widgets[stringVar+'-string'].set(dirname)
            self.settings[stringVar+'-string'] = dirname
        else:
            self.chooseDirectory("rldir")


    def verifyRLPath(self, dirname):
        verified = True
        if not self.verifyPath(dirname): verified = False; msg="Path does not exist."
        if len(dirname) < 12: verified = False; msg = "Directory path isn't long enough."
        if dirname[-12:] != "rocketleague": verified = False; msg = "Folder name is not 'rocketleague'"
        print(dirname, self.rldir_relpath)
        print(os.path.join(dirname, self.rldir_relpath))
        if not self.verifyPath(os.path.join(dirname,self.rldir_relpath)): verified = False; msg = "Folder '"+self.rldir_relpath+"' not found in directory."

        if not verified:
            mb.showerror(title="Error", message=msg+"\nTry again. (Check C:\\Program Files\\Epic Games)")

        return verified


    def confirmAction(self, title, message):
        return mb.askyesno(title=title, message=message)


    def clearSettings(self):
        for string in self.settings.keys():
            if string != "rldir-string":
                self.widgets[string].set(None)


    def writeSaveFile(self):
        with open("./maps.merl", "w") as f:
            json.dump(self.settings, f)


    def saveSettings(self):
        if not self.confirmAction(title="Save & Apply?", message="Are you sure you want to save and apply maps?"):
            return
        # backup original maps, if not yet backed up.
        self.backupMaps()
        # verify paths; show error & return if not found (skip for None's).
        verified = True
        notVerified = ""
        for string in self.settings.keys():
            if not self.verifyPath(self.settings[string]) and self.settings[string] != None \
                and self.settings[string] != "":
                verified = False
                self.widgets[string[:-7]+"-entry"].configure(foreground="red")
                notVerified += (string[:-7]+"\n").title()
            else:
                self.widgets[string[:-7]+"-entry"].configure(foreground="black")
        if not verified:
            mb.showerror(title="Error", message="One or more chosen files does not exist:\n"+notVerified)
            return
        # # direct-copy for upk/udk files (restore original for None's)
        # pass
        # # unzip, copy upk/udk for zip files (restore original for None's)
        # pass
        # write chosen maps to self.settings
        ## considering moving this to when it actually gets changed.
        # for string in self.settings.keys():
        #     self.settings[string] = self.widgets[string].get()

        # write self.settings to maps.merl
        self.writeSaveFile()

root = tk.Tk()
merl = Merl(root)
root.mainloop()