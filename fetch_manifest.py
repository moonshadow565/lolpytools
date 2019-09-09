#!/bin/env python
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

def main(args):
    parser = argparse.ArgumentParser(description='Fetch league releasemanifest')
    parser.add_argument('--cdn', type=str, default='http://akacdn.riotgames.com/releases', help='cdn url')
    parser.add_argument('--realm', type=str, default='live', help='realm')
    parser.add_argument('--project', type=str, default='lol_game_client', help='project')
    parser.add_argument('version', type=str, help='version to download')
    parser.add_argument('outfile', nargs='?', default='-', help='output .json')
    args = parser.parse_args()
    args.version = [ str(int(x)) for x in args.version.split('.') ]
    args.version = [ "0" ] * (4 - len(args.version)) + args.version
    args.version = '.'.join(args.version)
    url_prefix = "%s/%s/projects/%s" % (args.cdn, args.realm, args.project)
    url_man = "%s/releases/%s/releasemanifest" % (url_prefix, args.version)
    outfile = None
    if args.outfile == '-':
        outfile = io.BytesIO(sys.stdout.buffer)
    else:
        outdir = dirname(args.outfile)
        if outdir:
            makedirs(outdir, exist_ok=True)
        outfile = open(args.outfile, 'wb')
    data = urllib.request.urlopen(url_man).read()
    outfile.write(data)
    outfile.close()
    
if __name__ == '__main__':
    main(sys.argv[1:])
