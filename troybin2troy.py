#!/bin/env python
from lolpytools.convert import troybin2troy
import argparse
import sys
import json
import io

def main(args):
    parser = argparse.ArgumentParser(description='Convert league .troybin to .troy')
    parser.add_argument('infile', type=str, help='input .troybin file name')
    parser.add_argument('outfile', nargs='?', default='-', type=str, help='output .troy file name')
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
    troybin2troy(infile, outfile)

if __name__ == '__main__':
    main(sys.argv[1:])

