#!/bin/env python
import sys
import os
import time
from lolpytools.convert import luaobj2lua
from tkinter import filedialog
from tkinter import *


root = Tk()
root.title="Luaobj converter"
root.withdraw()
inname = filedialog.askopenfilename(title = "Open.luaobj file", filetypes = (("luaobj files","*.luaobj"),("all files","*.*")))
if os.path.isfile(inname):
    defoutname = os.path.basename(inname)
    print(defoutname)
    if defoutname.endswith(".luaobj"):
        defoutname = defoutname.replace('.luaobj', '.lua')
    else:
        defoutname = defoutname + '.lua'
    outname = filedialog.asksaveasfilename(title = "Save .lua file", initialfile=defoutname, filetypes = (("lua files","*.lua"),("all files","*.*")))
    with open(inname, 'rb') as infile:
        with open(outname, 'w', encoding='utf-8', newline='\r\n') as outfile:
            luaobj2lua(infile, outfile)
root.destroy()
