#!/usr/bin/env python
import struct
import io
import math
import re

#Hashes string if two given hashesh "section*name" (asterix included)
def ihash(section, name = None):
    if not name == None:
        section = section + '*' + name
    ret = 0
    for c in section:
        ret = (ord(c.lower()) +((65599 * ret) & 0xffffffff)) & 0xffffffff
    return ret

# Sanitize regexp's
RE_TRUE = re.compile(r"^\s*true\s*$", re.IGNORECASE);
RE_FALSE = re.compile(r"^\s*false\s*$", re.IGNORECASE);
RE_NAN = re.compile(r"^/s*NaN/s*$", re.IGNORECASE);
NAN_VALUE = float('nan')
RE_INT = re.compile(r"^\s*[-+]?\d+\s*$", re.IGNORECASE);
RE_DECIMAL = re.compile(r"^\s*[+-]?(?:\d+\.\d*|\d*\.\d+|\d+)(?:e[+-]?\d+)?\s*$", re.IGNORECASE);
RE_INT_VEC = re.compile(r"^\s*(?:[-+]?\d+\s+)+(?:[-+]?\d+)\s*$", re.IGNORECASE);
RE_DECIMAL_VEC = re.compile(r"^\s*(?:[+-]?(?:\d+\.\d*|\d*\.\d+|\d+)(?:e[+-]?\d+)?\s+)+([+-]?(?:\d+\.\d*|\d*\.\d+|\d+)(?:e[+-]?\d+)?)\s*$", re.IGNORECASE);

# converts values stored in string to their right value types
def sanitize_str(data):
    if RE_TRUE.match(data):
        return 1
    elif RE_FALSE.match(data):
        return 0
    elif RE_NAN.match(data):
        return NAN_VALUE
    elif RE_INT_VEC.match(data):
        return [int(x) for x in data.replace('\t', ' ').split(' ') if x]
    elif RE_DECIMAL_VEC.match(data):
        return [float(x) for x in data.replace('\t', ' ').split(' ') if x]
    elif RE_INT.match(data):
        return int(data)
    elif RE_DECIMAL.match(data):
        return float(data)
    else:
        return data
    
#Reads inibin from binary buffer to dictionary(keys and values in strings)
#Copies results to target and returns (optional argument)
def read_2(buffer, target):
    def read_flags(buffer, count):
        result = []
        bools = buffer.read(math.ceil(count/8))
        for index in range(0, count):
            result.append(bool((bools[index // 8] >> (index%8))  & 1))
        return result

    def read_numbers(buffer, fmt, count = 1, mul = 1):
        result = {}
        num = struct.unpack("<H", buffer.read(2))[0]
        keys = []
        for x in range(0, num):
            keys.append(struct.unpack("<I", buffer.read(4))[0])
        for x in range(0, num):
            tmp = []
            for y in range(0, count):
                tmp.append(struct.unpack(fmt, buffer.read(struct.calcsize(fmt)))[0] * mul)
            result[keys[x]] = tmp[0] if count == 1 else tmp
        return result

    def read_bools(buffer):
        result = {}
        num = struct.unpack("<H", buffer.read(2))[0]
        keys = []
        for x in range(0, num):
            keys.append(struct.unpack("<I", buffer.read(4))[0])
        bools = read_flags(buffer, num)
        for x in range(0, num):
            result[keys[x]] = int(bools[x])         
        return result

    def read_strings(buffer, stringsLength):
        result = {}
        offsets = read_numbers(buffer, "<H")
        data = buffer.read(stringsLength)
        for key in offsets:
            o = int(offsets[key])
            t = ""
            while data[o] != 0:
                t = t + chr(data[o])
                o = o + 1
            result[key] = sanitize_str(t)
        return result
    stringsLength = struct.unpack("<H", buffer.read(2))[0]
    flags = read_flags(buffer, 16)
    read_conf = [
        [read_numbers, ["<i"]],           #0  - 1 x int
        [read_numbers, ["<f"]],           #1  - 1 x float 
        [read_numbers, ["<B", 1, 0.1]],   #2  - 1 x byte * 0.1
        [read_numbers, ["<h"]],           #3  - 1 x short
        [read_numbers, ["<B"]],           #4  - 1 x byte 
        [read_bools, []],                 #5  - 1 x bools 
        [read_numbers, ["<B", 3, 0.1]],   #6  - 3 x byte * 0.1
        [read_numbers, ["<f", 3]],        #7  - 3 x float
        [read_numbers, ["<B", 2, 0.1]],   #8  - 2 x byte * 0.1
        [read_numbers, ["<f", 2]],        #9  - 2 x float
        [read_numbers, ["<B", 4, 0.1]],   #10 - 4 x byte * 0.1
        [read_numbers, ["<f", 4]],        #11 - 4 x float
        [read_strings, [stringsLength]],  #12 - strings
        # TODO: are strings stored at the end of file allways??
        #[read_numbers, ["<q"]],           #13 - long long
    ]
    for x in range(0, 16):
        if flags[x]:
            if x < len(read_conf):
                target.update(read_conf[x][0](buffer, *(read_conf[x][1])))
            else:
                raise "Unknown inibin flag {} in {}!".format(x, buffer.name)
    return target

# reads version 1 .inibin
def read_1(buffer, target):
    buffer.read(3)
    entryCount = struct.unpack("I", buffer.read(4))[0]
    dataCount = struct.unpack("I", buffer.read(4))[0]
    offsets = {}
    for i in range(0, entryCount):
        h = struct.unpack("I", buffer.read(4))[0]
        o = struct.unpack("I", buffer.read(4))[0]
        offsets[h] = o
    data = buffer.read(dataCount)
    result = {}
    for key in offsets:
        o = int(offsets[key])
        t = ""
        while data[o] != 0:
            t = t + chr(data[o])
            o = o + 1
        result[key] = sanitize_str(t)
    target.update(result)
    return target

# reads .inibin from bianry buffer with auto-detecting version
def read(buffer, result = None):
    if result == None:
        result = {
            "Values": {},
            "UNKNOWN_HASHES": {}
        }
    else:
        if not "Values" in result:
            result["Values"] = {}
        if not "UNKNOWN_HASHES" in result:
            result["UNKNOWN_HASHES"] = {}
    target = result["UNKNOWN_HASHES"]
    version = struct.unpack("B", buffer.read(1))[0]
    if version == 2:
        read_2(buffer, target)
    elif version == 1:
        read_1(buffer, target)
    else:
        raise "Unknow version!"
    return result
    
# reads .inibin from binary file on filesystem
def from_file(name, result = None):
    with open(name, "rb") as buffer:
        return read(buffer, result)

# gets entry in .ini/.inibin
def get(target, section, name, default = None):
    if section in target["Values"] and name in target["Values"][section]:
        return target["Values"][section][name]
    else:
        h = ihash(section, name)
        return target["UNKNOWN_HASHES"][h] if h in target["UNKNOWN_HASHES"] else default

