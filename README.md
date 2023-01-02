# merl
Map Editor for Rocket League

This python script allows you to edit your Epic Games version of Rocket League Lab Maps to use custom training maps, gotten from Steam.
It is currently considered to be in Alpha state.

# Version 1.8.0
This program uses [Semantic Versioning](http://semver.org)

# UPDATES
2023-01-01 - I found this! http://rocketleaguemaps.us/ and this new version updates the Map Download link to point there.

2022-08-08 - It has come to my attention that the nice folks at [Steam Workshop Downloader](https://steamworkshopdownloader.io/) have stopped providing the download service, at the behest of Valve; this makes the original instructions invalid, since you can no longer download steam maps this way. However, there are map creators that provide their map files separately - one that I know of is [Lethamyr](https://lethamyr.com/mymaps).

# TODO
 === \(100%\) ===
 - [x] - Write python Tkinter interface
 - [x] - Allow UPK/UDK file choosing
 - [x] - Allow ZIP file choosing
 - [x] - Code to reset map settings 
 - [x] - Code to restore settings from mapper.txt
 - [x] - Code to save settings
 - [x] - Code backup logic of original maps
 - [x] - Code replace logic for UPK/UDK
 - [x] - Code replace logic for ZIP file extract
 - [x] - Code restore logic if map slot is empty
 - [x] BUG - Save settings code only saving map settings loaded at beginning of session.


# Disclaimer
This software comes with absolutely no warranty. Using this software as intended will replace files in your Rocket League installation directory, which has the potential to break your installation. Please be aware of this before using it. That said, many people use the method that this program uses to play custom maps, so it may be relatively safe to use.

If your install of Rocket League quits working after using this program, you should be able to fix it by opening your Epic Games Launcher and going to your Library, clicking the three-dots next to Rocket League and then clicking Verify.

# Installation
If you have python installed on your computer, you should be able to clone the repository and run the source script merl.py as-is (from its own directory).

You may need to install the additional libraries `pillow` and `pypiwin32` with the command `pip install <library>` for each one (or `python -m pip install <library>`).

If you do not, or are not sure, you should be able to download the merl.zip file, extract it, and run merl.exe

# Using merl
## Before you Run
You have to download the map packs you want from Steam before using this. You can use [Steam Workshops](https://steamcommunity.com/app/252950/workshop/) to find workshop maps that you'd like to try out, and the copy the URL from the address bar and go to the [Steam Workshop Downloader](https://steamworkshopdownloader.io/) to download. Just paste the URL from the workshop page and click Download.

Remember where you save the file; most browsers place the file into `C:\Users\<user>\Downloads`

## Running merl
NOTE: You should NOT run merl while Rocket League is running.

Run the script (or exe). You'll be presented with a directory selector and a list of maps you can edit, with file choosers below them.

NOTE: If you run the EXE file, a command prompt will pop up, this is normal. Don't close it while running the program.

Use the directory selector to find your Rocket League installation directory. Usually it is located in `C:\Program Files\Epic Games\rocketleague` but you may have installed it elsewhere, possibly.

Once done, choose a map to edit. Use the Browse button under it to select the downloaded Steam map ZIP file, or UDK/UPK file inside it.

When done, click Save & Apply and merl will replace the selected map(s) with the chosen training pack(s).

NOTE: when you click Save & Apply, merl will attempt to backup the original map files before replacing them. It does this by moving the original file name to the same name with a .merl extention. IF YOU HAVE already replaced map files, it will "accidentally" backup those replaced files instead - if you revert for a map where this happened, it will revert back to those replaced maps, not the original one.

## Reverting Maps
To revert maps back to normal, clear the text box underneath it and click Save & Apply.

# Files
merl creates a small tracker text file linking the maps to the replacement files in the same directory it is located called `mapper.txt`

# Uninstalling
To uninstall merl, you can just delete the script folder. I'd recommend clearing maps and hitting Save & Apply first.

# Troubleshooting / Issues
1. Help! my map isn't working anymore!
  - Rocket League probably updated. Just open merl and click Save & Apply to reset your maps.
  - NOTE: it is possible that Rocket League may have changed filenames! If you apply a map and it doesn't work, please open an Issue here so I can check it out!
2. Help! I can't see any files in the file chooser box!
  - Check the file types in the bottom right-corner of the box, switch it to UPK, UDK, or ZIP as needed.
3. It says permission denied in the console? What's going on?
  - Rocket League can't be open while running merl. It may have the map files open, so we can't replace them.
4. not sure what else could go wrong? Let me know!

# License
This software is released under the GPL v3.0
