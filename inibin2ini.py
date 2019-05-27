#!/bin/env python
from lolpytools.convert import inibin2ini
import argparse
import sys
import json
import io

def main(args):
    parser = argparse.ArgumentParser(description='Convert league .inibin to .ini')
    parser.add_argument('infile', type=str, help='input .inibin file name')
    parser.add_argument('outfile', nargs='?', default='-', type=str, help='output .ini file name')
    args = parser.parse_args()
    infile = None
    outfile = None
    if args.infile == '-':
        infile = sys.stdin.buffer
    else:
        infile = open(args.infile, 'rb')
    if args.outfile == '-':
        outfile = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', newline='\r\n')
    else:
        outfile = open(args.outfile, 'w', encoding='utf-8', newline='\r\n')
    inibin2ini(infile, outfile)

if __name__ == '__main__':
    main(sys.argv[1:])

