#!/bin/env python
import sys
import argparse
from lolpytools.inibin import ihash

def main(args):
    parser = argparse.ArgumentParser(description='Makes a league inibin hash')
    parser.add_argument('section', type=str)
    parser.add_argument('name', type=str)
    args = parser.parse_args()
    print(ihash(args.section, args.name))

if __name__ == '__main__':
    main(sys.argv[1:])
