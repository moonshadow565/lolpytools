#!/bin/env python
from . import inibin
from . import inibin_fix

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
