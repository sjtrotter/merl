#!/usr/bin/env python3

import os
import shutil
import webbrowser
import zipfile
import win32api
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image

maps = {}
rldir = ""
rldir_relpath = "\\TAGame\\CookedPCConsole\\"
rldir_entry = ""
pillars_entry = ""
cosmic_entry = ""
double_entry = ""
underpass_entry = ""
utopia_entry = ""
octagon_entry = ""

filenames = {
    "Pillars":  ["Labs_CirclePillars_P.upk"],
    "Cosmic":   ["Labs_Cosmic_V4_P.upk", "Labs_Cosmic_P.upk"],
    "Double":   ["Labs_DoubleGoal_V2_P.upk", "Labs_DoubleGoal_P.upk"],
    "Underpass":["Labs_Underpass_P.upk", "Labs_Underpass_v0_p.upk"],
    "Utopia":   ["Labs_Utopia_P.upk"],
    "Octagon":  ["Labs_Octagon_02_P.upk","Labs_Octagon_P.upk"]
}

def loadMaps():
    global maps
    with open("mapper.txt") as mapper:
        for line in mapper:
            (k, v) = line.strip().split("|")
            maps[k] = v

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in dirs:
            return os.path.join(root, name)

def clearSettings():
    if (messagebox.askyesno(message="Are you sure you want to clear ALL your Map settings?", title="Clear Settings")):
            #RLDir.set(maps["rldir"])
            Pillars.set("")
            Cosmic.set("")
            Double.set("")
            Underpass.set("")
            Utopia.set("")
            Octagon.set("")

def saveMaps():
    global maps
    with open("mapper.txt", "w") as mapper:
        for key in maps.keys():
            if key != "rldir":
                maps[key] = file_entry_map[key][0].get()
            if maps[key] == "":
                maps[key] = "None"
            mapper.write(key+"|"+maps[key]+"\n")

def backupOriginals():
    path = find("CookedPCConsole",RLDir.get())
    for key in filenames.keys():
        for file in filenames[key]:
            fullpath = path + "\\" + file
            if not(os.path.isfile(fullpath+".merl")):
                shutil.copyfile(fullpath, fullpath+".merl")
            else:
                print(file + ".merl exists, skipping...")

def restoreOriginal(filenames):
    for file in filenames:
        orig_filename = os.path.join(RLDirFullPath, file)
        print("Restoring "+orig_filename+"...")
        shutil.copyfile(orig_filename+".merl", orig_filename)


def saveSettings():
    global file_entry_map
    global RLDirFullPath

    RLDirFullPath = find("CookedPCConsole",RLDir.get())
    file_entry_map = {
        "Pillars": [Pillars, pillars_entry],
        "Cosmic": [Cosmic, cosmic_entry],
        "Double": [Double, double_entry],
        "Underpass": [Underpass, underpass_entry],
        "Utopia": [Utopia, utopia_entry],
        "Octagon": [Octagon, octagon_entry]
    }
    if (RLDir.get() == "" or find("CookedPCConsole",RLDir.get()) == None or RLDir.get()[-12:] != "rocketleague"):
        messagebox.showerror(message="Error: Either the RL Location is blank, or the path given does not contain the CookedPCConsole folder with the maps in it.\nPlease check the RL Location and try again.",
                            title="Incorrect or Missing RL Location")
        rldir_entry.configure(foreground="red")
        return
    rldir_entry.configure(foreground="black")

    

    if (messagebox.askyesno(message="This will save settings and apply changes. Okay?", title="Save & Apply Settings")):
        err_condition = 0
        err_message = ""

        backupOriginals()

        for key in filenames.keys():
            new_file = file_entry_map[key][0].get()
            print(new_file)
            if new_file != "":
                file_ext = new_file[-4:].lower()
                print(file_ext)
                if not(file_ext == ".upk" or file_ext == ".udk" or file_ext == ".zip"):
                    messagebox.showerror(message="Error: "+new_file+" for "+key+" is not a UPK, UDK, or ZIP file.\nPlease check the Map Location and try again.",
                        title="Incorrect Map File Extension")
                    file_entry_map[key][1].configure(foreground="red")
                    return
                if not(os.path.isfile(new_file)):
                    messagebox.showerror(message="Error: "+new_file+" for "+key+" does not exist.\nPlease check the Map Location and try again.",
                        title="Map File Doesn't Exist")
                    file_entry_map[key][1].configure(foreground="red")
                    return
            else:
                restoreOriginal(filenames[key])
            
            file_entry_map[key][1].configure(foreground="black")

        # direct copy of upk/udk file
        path = find("CookedPCConsole",RLDir.get())
        for key in filenames.keys():
            new_file = file_entry_map[key][0].get()
            print(new_file)
            file_ext=new_file[-4:].lower()
            if file_ext == ".upk" or file_ext == ".udk":
                for file in filenames[key]:
                    fullpath = os.path.join(RLDirFullPath, file)
                    if os.path.isfile(new_file):
                        shutil.copyfile(new_file, fullpath)

        # extract upk/udk from zip & copy
            elif file_ext == ".zip":
                try:
                    zf = zipfile.ZipFile(new_file)
                    print(zf.namelist())
                    count = 0
                    zfile = ""
                    for zippedfile in zf.namelist():
                        zf_ext = zippedfile[-4:].lower()
                        if zf_ext == ".upk" or zf_ext == ".udk":
                            zf.extract(zippedfile, "zip_tmp")
                            zfile = zippedfile
                            count += 1
                    zf.close()

                    if count != 1:
                        raise

                    for file in filenames[key]:
                        fullpath = path + "\\" + file
                        extracted_file = os.path.join(".","zip_tmp",zfile)
                        if os.path.isfile(extracted_file):
                            shutil.copyfile(extracted_file, fullpath)
                    shutil.rmtree("zip_tmp")

                except:
                    messagebox.showerror(message="There was an issue opening "+new_file+" for "+key+".\n You can try: \n\
 - checking to make sure you selected the right ZIP file\n\
 - extracting the archive and selecting the correct UPK/UDK file instead",
                        title="Error Extracting from ZIP")
                    return

        saveMaps()

        if err_condition == 0:
            messagebox.showinfo(message="Changes successfully saved and applied!", title="Save & Apply Settings")
        else:
            messagebox.showerror(message=err_message,
                    title="Error Saving & Applying")
    else:
        messagebox.showerror(message="Changes not saved or applied.",
                    title="Save & Apply Cancelled")

def browseFiles(initdir):
    filename = filedialog.askopenfilename(  initialdir=initdir,
                                            title="Select Map",
                                            filetypes=(("Map Files upk", "*.upk"),
                                                        ("Map Files udk", "*.udk"),
                                                        ("ZIP Files", "*.zip")))
    return filename

def rldir_browseFiles():
    dirname = filedialog.askdirectory( initialdir=os.path.split(RLDir.get()),
                                        title="Rocket League Directory?")
    if dirname != "":
        RLDir.set(dirname)
    
def pillars_browseFiles():
    filename = browseFiles(os.path.split(Pillars.get()))
    if filename != "":
        Pillars.set(filename)

def cosmic_browseFiles():
    filename = browseFiles(os.path.split(Cosmic.get()))
    Cosmic.set(filename)

def double_browseFiles():
    filename = browseFiles(os.path.split(Double.get()))
    if filename != "":
        Double.set(filename)

def underpass_browseFiles():
    filename = browseFiles(os.path.split(Underpass.get()))
    if filename != "":
        Underpass.set(filename)

def utopia_browseFiles():
    filename = browseFiles(os.path.split(Utopia.get()))
    if filename != "":
        Utopia.set(filename)

def octagon_browseFiles():
    filename = browseFiles(os.path.split(Octagon.get()))
    if filename != "":
        Octagon.set(filename)

def link_click(url):
    webbrowser.open_new_tab(url)

def mainloop():
    root = Tk()
    root.title("Map Editor for Rocket League")

    mainframe = ttk.Frame(root)
    mainframe.grid(column=0, row=0, sticky=("nsew"))

    for key in maps.keys():
        if maps[key] == "None":
            maps[key] = ""

    global RLDir
    global Pillars
    global Cosmic
    global Double
    global Underpass
    global Utopia
    global Octagon

    RLDir = StringVar()
    Pillars = StringVar()
    Cosmic = StringVar()
    Double = StringVar()
    Underpass = StringVar()
    Utopia = StringVar()
    Octagon = StringVar()

    RLDir.set(maps["rldir"])
    Pillars.set(maps["Pillars"])
    Cosmic.set(maps["Cosmic"])
    Double.set(maps["Double"])
    Underpass.set(maps["Underpass"])
    Utopia.set(maps["Utopia"])
    Octagon.set(maps["Octagon"])

    global rldir_entry
    global pillars_entry
    global cosmic_entry
    global double_entry
    global underpass_entry
    global utopia_entry
    global octagon_entry

    rldir_label = ttk.Label(mainframe, justify="right", padding=3, font=('Arial Bold', 9),
        text="RL Location (i.e. C:\\Program Files\\Epic Games\\rocketleague) :")
    pillarImg = ImageTk.PhotoImage(Image.open("pillars.png"))
    pillars_label = ttk.Label(mainframe, image=pillarImg)
    cosmicImg = ImageTk.PhotoImage(Image.open("cosmic.png"))
    cosmic_label = ttk.Label(mainframe, image=cosmicImg)
    doubleImg = ImageTk.PhotoImage(Image.open("double.png"))
    double_label = ttk.Label(mainframe, image=doubleImg)
    underpassImg = ImageTk.PhotoImage(Image.open("underpass.png"))
    underpass_label = ttk.Label(mainframe, image=underpassImg)
    utopiaImg = ImageTk.PhotoImage(Image.open("utopia.png"))
    utopia_label = ttk.Label(mainframe, image=utopiaImg)
    octagonImg = ImageTk.PhotoImage(Image.open("octagon.png"))
    octagon_label = ttk.Label(mainframe, image=octagonImg)
    
    rldir_entry = ttk.Entry(mainframe, width=40, textvariable=RLDir)
    pillars_entry = ttk.Entry(mainframe, width=30, textvariable=Pillars)
    cosmic_entry = ttk.Entry(mainframe, width=30, textvariable=Cosmic)
    double_entry = ttk.Entry(mainframe, width=30, textvariable=Double)
    underpass_entry = ttk.Entry(mainframe, width=30, textvariable=Underpass)
    utopia_entry = ttk.Entry(mainframe, width=30, textvariable=Utopia)
    octagon_entry = ttk.Entry(mainframe, width=30, textvariable=Octagon)

    rldir_browse = ttk.Button(mainframe, width=10, text="Browse", padding=3, command=rldir_browseFiles)
    pillars_browse = ttk.Button(mainframe, text="Browse", padding=3, command=pillars_browseFiles)
    cosmic_browse = ttk.Button(mainframe, text="Browse", padding=3, command=cosmic_browseFiles)
    double_browse = ttk.Button(mainframe, text="Browse", padding=3, command=double_browseFiles)
    underpass_browse = ttk.Button(mainframe, text="Browse", padding=3, command=underpass_browseFiles)
    utopia_browse = ttk.Button(mainframe, text="Browse", padding=3, command=utopia_browseFiles)
    octagon_browse = ttk.Button(mainframe, text="Browse", padding=3, command=octagon_browseFiles)
    clear_settings = ttk.Button(mainframe, text="Clear Maps", padding=5, command=clearSettings)
    save_settings = ttk.Button(mainframe, text="Save & Apply", padding=5, command=saveSettings)

    steam_link = Label(mainframe, justify="center", text="Steam Workshop Maps",font=('Helveticabold', 12), fg="blue", cursor="hand2")
    steam_dl_link = Label(mainframe, justify="center", text="Steam Workshop Downloader",font=('Helveticabold', 12), fg="blue", cursor="hand2")

    steam_link.bind("<Button-1>", lambda e: link_click("https://steamcommunity.com/app/252950/workshop/"))
    steam_dl_link.bind("<Button-1>", lambda e: link_click("https://steamworkshopdownloader.io/"))

    steam_link.grid(column=0, row=0, columnspan=2, sticky=(N,E,S,W))
    steam_dl_link.grid(column=2, row=0, columnspan=2, sticky=(N,S,E,W))
    rldir_label.grid(column=0, row=1, columnspan=2, sticky=(E))
    rldir_entry.grid(column=2, row=1, columnspan=1, sticky=(N,S,W,E))
    rldir_browse.grid(column=3, row=1, sticky=(W,E))
    pillars_label.grid(column=0, row=2, columnspan=2, sticky=(N,W,E,S))
    cosmic_label.grid(column=2, row=2, columnspan=2, sticky=(N,W,E,S))
    pillars_entry.grid(column=0, row=3, sticky=(W,E,N,S))
    pillars_browse.grid(column=1, row=3, sticky=(W,E))
    cosmic_entry.grid(column=2, row=3, sticky=(W,E,N,S))
    cosmic_browse.grid(column=3, row=3, sticky=(W,E))
    double_label.grid(column=0, row=4, columnspan=2, sticky=(N,W,E,S))
    underpass_label.grid(column=2, row=4, columnspan=2, sticky=(N,W,E,S))
    double_entry.grid(column=0,row=5,sticky=(W,E,N,S))
    double_browse.grid(column=1, row=5, sticky=(W,E))
    underpass_entry.grid(column=2,row=5,sticky=(W,E,S,N))
    underpass_browse.grid(column=3, row=5, sticky=(W,E))
    utopia_label.grid(column=0, row=6, columnspan=2, sticky=(N,W,E,S))
    octagon_label.grid(column=2,row=6, columnspan=2, sticky=(N,W,E,S))
    utopia_entry.grid(column=0, row=7, sticky=(W,E,S,N))
    utopia_browse.grid(column=1, row=7, sticky=(W,E))
    octagon_entry.grid(column=2, row=7, sticky=(W,E,S,N))
    octagon_browse.grid(column=3, row=7, sticky=(W,E))
    clear_settings.grid(column=0, row=8, columnspan=2, sticky=(E,W))
    save_settings.grid(column=2, row=8, columnspan=2, sticky=(E,W))


    root.mainloop()



if not(os.path.isfile("mapper.txt")):
    with open("mapper.txt","w") as mapper:
        mapper.write("rldir|None\n")
        mapper.write("Pillars|None\n")
        mapper.write("Cosmic|None\n")
        mapper.write("Double|None\n")
        mapper.write("Underpass|None\n")
        mapper.write("Utopia|None\n")
        mapper.write("Octagon|None\n")

loadMaps()
#print(maps)
rldir = maps["rldir"]
if rldir == "None":
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    #print(drives)

    rldir = ""
    for drive in drives:
        rldir = find("rocketleague",drive + "Program Files")
        if rldir != None:
            break
    if rldir == "":
        print("Rocket League directory not found...")
    else:
        maps["rldir"] = rldir;

mainloop()