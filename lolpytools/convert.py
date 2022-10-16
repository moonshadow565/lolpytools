#!/bin/env python
from . import inibin2
from . import inibin_fix
from . import troybin_fix
from . import plua
import json

def rrepr(value):
    # Otherwise, the League does not read colors
    if isinstance(value, float) and value % 1 == 0:
        return str(int(value))
    return repr(value)

def writeini(ibin, outfile):
    def write_value(name, value):
        if isinstance(value, str):
            outfile.write('{}={}\n'.format(name, value))
        elif isinstance(value, bool):
            outfile.write('{}={}\n'.format(name, 'true' if value else 'false'))
        elif isinstance(value, list) or isinstance(value, tuple):
            outfile.write('{}={}\n'.format(name, ' '.join([rrepr(x) for x in value])))
        elif isinstance(value, int):
            outfile.write('{}={}\n'.format(name, value))
        elif isinstance(value, float):
            outfile.write('{}={}\n'.format(name, rrepr(value)))
        else:
            raise Exception("Unknown type: {}".format(type(value)))
    for section, names in sorted(ibin["Values"].items()):
        outfile.write('[{}]\n'.format(section))
        for name, value in sorted(names.items()):
            write_value(name, value)
        outfile.write('\n')
    if len(ibin["UNKNOWN_HASHES"]) > 0:
        outfile.write('[UNKNOWN_HASHES]\n')
        for name, value in sorted(ibin["UNKNOWN_HASHES"].items(), key=lambda kv: f'{kv[0]:08X}'):
            write_value("unk{:08X}".format(int(name)), value)

def inibin2ini(infile, outfile):
    ibin = inibin2.read(infile)
    inibin_fix.fix(ibin)
    writeini(ibin, outfile)

def troybin2troy(infile, outfile):
    ibin = inibin2.read(infile)
    troybin_fix.fix(ibin)
    writeini(ibin, outfile)

def writelua(lua, outfile):
    g = lua["Values"]
    
    def verify_array(value):
        sz = len(value) + 1
        if 0 in value:
            return False
        for i in range(1, sz):
            if not i in value:
                return False
        return True
    
    def write_value(value, indent = 0):
        if value is None:
            outfile.write("nil")
        elif isinstance(value, str):
            if value.startswith("~~"):
                outfile.write(value[2:])
            else:
                outfile.write(json.dumps(value))
        elif isinstance(value, int):
            outfile.write(str(value))
        elif isinstance(value, float):
            outfile.write(repr(value))
        elif isinstance(value, bool):
            outfile.write("True" if value else "False")
        elif isinstance(value, dict):
            if len(value) == 0:
                outfile.write("{}")
            else:
                outfile.write("{\n")
                isarray = verify_array(value)
                #TODO: Find out why the error occurs
                #for tkey, tvalue in sorted(value.items()):
                for tkey, tvalue in value.items():
                    outfile.write(" " * ((indent + 1) * 4))
                    if not isarray:
                        outfile.write("[")
                        write_value(tkey, indent + 1)
                        outfile.write("] = ")
                    write_value(tvalue, indent + 1)
                    outfile.write(",\n")
                outfile.write(" " * (indent * 4))
                outfile.write("}")
            pass
        else:
            raise Exception("Unknown type: {}".format(type(value))) 
    for gname, gvalue in sorted(g.items()):
        outfile.write("{} = ".format(gname))
        write_value(gvalue, 0)
        outfile.write("\n")
        
def luaobj2lua(infile, outfile):
    writelua(plua.read(infile), outfile)
