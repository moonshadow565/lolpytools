import os
import re
import os.path
import json
import inibin
def all(directory = "X:/lol/420inibin/"):
    rx = re.compile(".+/DATA/Characters/(?:.+/Skins/)?([^/]+)/\\1\\.inibin$", re.IGNORECASE)
    #rx = re.compile(".+/DATA/Items/[^\\/]+\\.inibin$", re.IGNORECASE)
    #rx = re.compile(".+/DATA/(.+/)?Spells/[^\\/]+\\.inibin$", re.IGNORECASE)
    #rx = re.compile(".+/(?:DATA|DATA/Characters/[^/]+|DATA/Shared|DATA/Talents)/Spells/[^\\/]+\\.inibin$", re.IGNORECASE)
    result = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file).replace("\\","/")
            #relp = os.path.relpath(path, directory)
            if rx.match(path):
                inibin.from_file(path, result)
                inibin.fix_inibin(result)
    return result
def all2(directory = "X:/lol/420inibin/"):
    #rx = re.compile(".+/DATA/Characters/(?:.+/Skins/)?([^/]+)/\\1\\.inibin$", re.IGNORECASE)
    #rx = re.compile(".+/DATA/Items/[^\\/]+\\.inibin$", re.IGNORECASE)
    rx = re.compile(".+/DATA/(.+/)?Spells/[^\\/]+\\.inibin$", re.IGNORECASE)
    #rx = re.compile(".+/(?:DATA|DATA/Characters/[^/]+|DATA/Shared|DATA/Talents)/Spells/[^\\/]+\\.inibin$", re.IGNORECASE)
    result = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file).replace("\\","/")
            relp = os.path.relpath(path, directory)
            if rx.match(path):
                r = inibin.from_file(path)
                inibin.fix_inibin(r)
                u = copyunk(r)
                if len(u["UNKNOWN_HASHES"]) > 0:
                    result[relp] = u["UNKNOWN_HASHES"]
    return result


def all3(directory = "X:/lol/420troybin/"):
    rx = re.compile(".+/DATA(.*/)Particles/[^\\/]+\\.troybin$", re.IGNORECASE)
    result = { "Values": {}, "UNKNOWN_HASHES": {}, "Sections":[] }
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file).replace("\\","/")
            relp = os.path.relpath(path, directory)
            if rx.match(path):
                tbin = inibin.from_file(path)
                sections = inibin.fix_troybin_sections(tbin)
                for section in sections:
                    section = section.lower()
                    if not section in result["Sections"]:
                        result["Sections"].append(section)
                inibin.fix_troybin(tbin)
                for section in tbin["Values"]:
                    for name in tbin["Values"][section]:
                        if not section in result["Values"]:
                            result["Values"][section] = {}
                        result["Values"][section][name] = tbin["Values"][section][name]
                for unk in tbin["UNKNOWN_HASHES"]:
                    result["UNKNOWN_HASHES"][unk] = tbin["UNKNOWN_HASHES"][unk]
                
    return result
def all4(directory = "X:/lol/420troybin/"):
    rx = re.compile(".+/DATA(.*/)Particles/[^\\/]+\\.troybin$", re.IGNORECASE)
    result = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file).replace("\\","/")
            #relp = os.path.relpath(path, directory)
            if rx.match(path):
                tbin = inibin.from_file(path)
                sections = inibin.fix_troybin_sections(tbin)
                for s in sections:
                    s = str(s).lower()
                    if not s in result:
                        result.append(s)
    return result

def twitch():
    t = inibin.from_file("twitch_sprayandPray_mis.troybin")
    inibin.fix_troybin(t)
    return t

def countunk(i):
    return len(i["UNKNOWN_HASHES"])
def ihash(name):
    ret = 0
    for c in name:
        ret = (ord(c) +((65599 * ret) & 0xffffffff)) & 0xffffffff
    return ret
def test1(inib, name):
    h = ihash(name.lower())
    if h in inib["UNKNOWN_HASHES"]:
        print("Found!", name, h)
        return True
    return False
def test(inib, section, name):
    test1(inib, "{}*{}".format(section,name).lower())
    test1(inib, "{}*'{}".format(section,name).lower())
    test1(inib, "{}**{}".format(section,name).lower())
    test1(inib, name.lower())
    test1(inib, "'{}".format(name).lower())
    test1(inib, "*{}".format(name).lower())
    if section in inib["Values"] and name in inib["Values"][section]:
        print("already in")
def testt(troy, name):
    if not "Sections" in troy:
        troy["Sections"] = inibin.fix_troybin_sections(troy)
    for section in troy["Sections"]:
        test(troy, section, name)
def testtarr(arr, name):
    for troy in arr:
        testt(troy, name)
        
def testtcomas(troy):
    if not "Sections" in troy:
        troy["Sections"] = inibin.fix_troybin_sections(troy)
    for section in troy["Sections"]:
        for name in inibin.fix_troybin_names:
            test1(troy, "{}*'{}".format(section, name))
            test1(troy, "{}**{}".format(section, name))
def testcomas(inib, fro):
    for sn in fro.items():
        test1(inib, "{}*'{}".format(sn[0], sn[1]))
        test1(inib, "{}**{}".format(sn[0], sn[1]))
def tojson(data):
    return inibin.to_json(data)
def jprint(data):
    print(tojson(data))
def save(what, data):
    f = open("{}.json".format(what), 'w')
    f.write(inibin.to_json(data))
    f.close()
def read(what):
    return open("{}.json".format(what), 'r').read()
def load(what):
    return json.loads(read(what))
def copyunk(data):
    return { "Values":{}, "UNKNOWN_HASHES": data["UNKNOWN_HASHES"].copy() }

def testinter(ini, section):
    while True:
        name = input()
        if name == "":
            break
        test(ini, section, name)
