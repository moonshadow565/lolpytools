import struct
import io
import re
import os
import json
import binascii
import sys
import time
from datetime import datetime


try:
    from itertools import izip as zip
except:
    pass

# majorV, minorV, projectNameIndex, releaseV
s_header = struct.Struct('< H H I I')

# uint32
s_count = struct.Struct('< I')

# uint32 uint32
s_names = struct.Struct('< I I')

# "NameIndex", "SubFolderStartIndex", "SubFolderCount", "FileListStartIndex", "FileCount"
s_folder = struct.Struct('< I I I I I')
class rel_folder:
    def __init__(self, buffer):
        data = s_folder.unpack_from(buffer.read(s_folder.size))
        self.NameIndex = data[0]
        self.SubFolders = range(data[1], data[1] + data[2])
        self.Files = range(data[3], data[3] + data[4])
        self.Name = ""
        self.Parent = None

# "NameIndex", "Version", 16*"MD5", "DeployMode", "SizeRaw", "SizeCompressed", "Date"
s_file = struct.Struct('< I 4B 16s I I I Q')
class rel_file:
    def __init__(self, buffer):
        data = s_file.unpack_from(buffer.read(s_file.size))
        self.NameIndex = data[0]
        self.Version = ".".join(str(x) for x in data[4:0:-1])
        self.MD5 = binascii.hexlify(data[5]).decode('utf-8')
        self.DeployMode = data[6]
        self.SizeRaw = data[7]
        self.SizeCompressed = data[8]
        self.Date = data[9]
        self.Name = ""
        self.Parent = None

def read(buffer):
    magic = buffer.read(4)
    def unpack(what):
        return what.unpack_from(buffer.read(what.size))
    if not magic == b"RLSM":
        raise "Wrong releasemanifest magic!"
    majorV, minorV, prNameIndex, releaseV, = unpack(s_header)
    folderC, = unpack(s_count)
    folders = [ rel_folder(buffer) for x in range(0, folderC) ]
    fileC, = unpack(s_count)
    files = [ rel_file(buffer) for x in range(0, fileC) ]
    nameC,namesL, = unpack(s_names)
    names = buffer.read(namesL).decode('utf-8').split('\0')
    for folder in folders:
        folder.Name = names[folder.NameIndex]
        for i in folder.SubFolders:
            folders[i].Parent = folder
        for i in folder.Files:
            files[i].Parent = folder
            files[i].Name = names[files[i].NameIndex]
    def path(entry):
        return "{}{}".format(path(entry.Parent)+"/" if entry.Parent else "", entry.Name)
    return {
        path(f) : {
            "Version" : f.Version,
            "MD5" : f.MD5,
            "SizeRaw" : f.SizeRaw,
            "SizeCompressed" : f.SizeCompressed,
            "Date": f.Date,
            "DeployMode": f.DeployMode,
        } for f in files
    }
    
def from_file(name):
    buffer = open(name, 'rb')
    return read(buffer)

def to_json(data):
    return json.dumps(data, indent=2)


