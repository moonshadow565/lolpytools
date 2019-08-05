#!/bin/env python
import sys
import os
import time
from lolpytools.convert import troybin2troy
from tkinter import filedialog
from tkinter import *


root = Tk()
root.title="troybin converter"
root.withdraw()
inname = filedialog.askopenfilename(title = "Open.troybin file", filetypes = (("troybin files","*.troybin"),("all files","*.*")))
if os.path.isfile(inname):
    defoutname = os.path.basename(inname)
    print(defoutname)
    if defoutname.endswith(".troybin"):
        defoutname = defoutname.replace('.troybin', '.troy')
    else:
        defoutname = defoutname + '.troybin'
    outname = filedialog.asksaveasfilename(title = "Save .troy file", initialfile=defoutname, filetypes = (("troy files","*.troy"),("all files","*.*")))
    with open(inname, 'rb') as infile:
        with open(outname, 'w', encoding='utf-8', newline='\r\n') as outfile:
            troybin2troy(infile, outfile)
root.destroy()
