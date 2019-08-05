#!/bin/env python
import sys
import os
import time
from lolpytools.convert import inibin2ini
from tkinter import filedialog
from tkinter import *


root = Tk()
root.title="Inibin converter"
root.withdraw()
inname = filedialog.askopenfilename(title = "Open.inibin file", filetypes = (("inibin files","*.inibin"),("all files","*.*")))
if os.path.isfile(inname):
    defoutname = os.path.basename(inname)
    print(defoutname)
    if defoutname.endswith(".inibin"):
        defoutname = defoutname.replace('.inibin', '.ini')
    else:
        defoutname = defoutname + '.inibin'
    outname = filedialog.asksaveasfilename(title = "Save .ini file", initialfile=defoutname, filetypes = (("ini files","*.ini"),("all files","*.*")))
    with open(inname, 'rb') as infile:
        with open(outname, 'w', encoding='utf-8', newline='\r\n') as outfile:
            inibin2ini(infile, outfile)
root.destroy()
