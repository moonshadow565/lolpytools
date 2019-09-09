#!/bin/env python
from lolpytools.releasemanifest import read
from os import makedirs
from os.path import dirname
import argparse
import sys
import json
import io
import re
import os
import os.path
import urllib.request
import zlib
from urllib.parse import quote


def main(args):
    parser = argparse.ArgumentParser(description='Fetch league files from releasemanifest')
    parser.add_argument('--cdn', type=str, default='http://akacdn.riotgames.com/releases', help='cdn url')
    parser.add_argument('--realm', type=str, default='live', help='realm')
    parser.add_argument('--project', type=str, default='lol_game_client', help='project')
    parser.add_argument('outdir', type=str, help='output directory')
    parser.add_argument('infile', nargs='?', type=str, default='-', help='manifest .json file')
    parser.add_argument('match', nargs='?', type=re.compile, default=None, help='regex filter')
    args = parser.parse_args()
    url_prefix = "%s/%s/projects/%s" % (args.cdn, args.realm, args.project)
    files = {}
    if args.infile == '-':
        infile = io.BytesIO(sys.stdout.buffer)
        files = read(infile)
    else:
        infile = open(args.infile, 'rb')
        files=  read(infile)
    for name, info in files.items():
        if args.match and not args.match.match(name):
            continue
        dstpath = args.outdir + '/' + name
        dstdir = dirname(dstpath)
        if dstdir:
            makedirs(dstdir, exist_ok=True)
        srcpath = "%s/releases/%s/files%s.compressed" % (url_prefix, info["Version"] ,quote(name))
        print("Fetching", srcpath)
        data = urllib.request.urlopen(srcpath).read()
        data = zlib.decompress(data)
        x = open(dstpath, "wb").write(data)

if __name__ == '__main__':
    main(sys.argv[1:])
