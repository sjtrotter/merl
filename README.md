# merl
Map Editor for Rocket League

This python script allows you to edit your Epic Games version of Rocket League Lab Maps to use custom training maps, gotten from Steam.

# Version 0.6.0
This program uses [Semantic Versioning](http://semver.org)

# TODO
 === \(60%\) ===
 - [x] - Write python Tkinter interface
 - [x] - Allow UPK/UDK file choosing
 - [x] - Allow ZIP file choosing
 - [x] - Code to reset map settings 
 - [x] - Code to restore settings from mapper.txt
 - [x] - Code to save settings
 - [x] - Code backup logic of original maps
 - [ ] - Code replace logic for UPK/UDK
 - [ ] - Code replace logic for ZIP file extract
 - [ ] - Code restore logic if map slot is empty


# Disclaimer
This software comes with absolutely no warranty. Using this software as intended will replace files in your Rocket League installation directory, which has the potential to break your installation. Please be aware of this before using it. That said, many people use the method that this program uses to play custom maps, so it may be relatively safe to use.

If your install of Rocket League quits working after using this program, you should be able to fix it by opening your Epic Games Launcher and going to your Library, clicking the three-dots next to Rocket League and then clicking Verify.

# Installation
If you have python installed on your computer, you should be able to download the source script and run it as-is.

You may need to install the additional libraries `pillow` and `pypiwin32` with the command `pip install <library>` for each one (or `python -m pip install <library>`).

If you do not, or are not sure, you should be able to download the merl.exe from the dist folder and run it.

# Using merl
## Before you Run
You have to download the map packs you want from Steam before using this. You can use [Steam Workshops](https://steamcommunity.com/app/252950/workshop/) to find workshop maps that you'd like to try out, and the copy the URL from the address bar and go to the [Steam Workshop Downloader](https://steamworkshopdownloader.io/) to download. Just paste the URL from the workshop page and click Download.

Remember where you save the file; most browsers place the file into `C:\Users\<user>\Downloads`

## Running merl
Run the script (or exe). You'll be presented with a directory selector and a list of maps you can edit, with file choosers below them (and a Revert button for each one).

Use the directory selector to find your Rocket League installation directory. Usually it is located in `C:\Program Files\Epic Games\rocketleague` but you may have installed it elsewhere, possibly.

Once done, choose a map to edit. Use the file chooser to select the downloaded Steam map ZIP file.

When done, click Replace and merl will replace the selected map(s) with the chosen training pack(s).

NOTE: when you click Replace, merl will attempt to backup the original map files before replacing them. It does this by moving the original file name to the same name with a .merl extention. IF YOU HAVE already replaced map files, it will "accidentally" backup those replaced files instead - if you click Revert for a map where this happened, it will revert back to those replaced maps, not the original one.

# Files
merl creates a small tracker text file linking the maps to the replacement files in the same directory it is located called `mapper.txt`

# Uninstalling
To uninstall merl, you can just delete the script or exe you downloaded.

# Troubleshooting / Issues
1. Help! my map isn't working anymore!
  - Rocket League probably updated. Just open merl and click Replace to reset your maps.
2. Help! I can't see any files in the file chooser box!
  - Check the file types in the bottom right-corner of the box, switch it to UPK, UDK, or ZIP as needed.
3. not sure what else could go wrong? Let me know!

# License
This software is released under the GPL v3.0
