#!/bin/env python
from lolpytools.inibin_fix import fix_dry
from lolpytools.inibin_fix import fix
import argparse
import sys
import json
import io

def main(args):
    parser = argparse.ArgumentParser(description='Convert league .inibin to .ini')
    parser.add_argument('infile', type=str, help='input .inibin file name')
    args = parser.parse_args()
    infile = None
    if args.infile == '-':
        infile = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    else:
        infile = open(args.infile, 'r')
    j = json.load(infile)
    j["Values"] = {}
    j["UNKNOWN_HASHES"] ={ int(k) : v for k,v in j["UNKNOWN_HASHES"].items() }
    fix(j)
    print(json.dumps(j["Values"], sort_keys=True, indent=2 ))
    print(len(j["UNKNOWN_HASHES"]))

if __name__ == '__main__':
    main(sys.argv[1:])
