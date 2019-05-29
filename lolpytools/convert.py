#!/bin/env python
from . import inibin
from . import inibin_fix
from . import plua
import json

def inibin2ini(infile, outfile):
    ibin = inibin.read(infile)
    inibin_fix.fix(ibin)
    def write_value(name, value):
        if isinstance(value, str):
            outfile.write('{}="{}"\n'.format(name, value))
        elif isinstance(value, bool):
            outfile.write('{}={}\n'.format(name, '1' if value else '0'))
        elif isinstance(value, list):
            outfile.write('{}={}\n'.format(name, ' '.join([str(x) for x in value])))
        else:
            outfile.write('{}={}\n'.format(name, value))
    for section, names in sorted(ibin["Values"].items()):
        outfile.write('[{}]\n'.format(section))
        for name,value in sorted(names.items()):
            write_value(name, value)
        outfile.write('\n')
    for name, value in sorted(ibin["UNKNOWN_HASHES"].items()):
        write_value(";UNKNOWN_HASH {}".format(name), value)

def luaobj2lua(infile, outfile):
    g = plua.read(infile)["Values"]
    
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
            outfile.write(json.dumps(value))
        elif isinstance(value, int):
            outfile.write(str(value))
        elif isinstance(value, float):
            outfile.write(str(value))
        elif isinstance(value, bool):
            outfile.write("True" if value else "False")
        elif isinstance(value, dict):
            if len(value) == 0:
                outfile.write("{}")
            else:
                outfile.write("{\n")
                isarray = verify_array(value)
                for tkey, tvalue in sorted(value.items()):
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
        
