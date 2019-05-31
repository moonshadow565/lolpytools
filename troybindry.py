#!/bin/env python
from lolpytools import troybin_fix
from lolpytools import inibin
import argparse
import sys
import json
import io

def main(args):
    parser = argparse.ArgumentParser(description='Convert league .troybin to .troy')
    parser.add_argument('infile', type=str, help='input .troybin file name')
    args = parser.parse_args()
    infile = None
    if args.infile == '-':
        infile = sys.stdin.buffer
    else:
        infile = open(args.infile, 'rb')
    tbin = inibin.read(infile)
    troybin_fix.fix(tbin)
    print(len(tbin["UNKNOWN_HASHES"]))

if __name__ == '__main__':
    main(sys.argv[1:])
