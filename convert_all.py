import os
import argparse
from tqdm.contrib.concurrent import process_map
from lolpytools.convert import inibin2ini, luaobj2lua, troybin2troy
import re
import traceback

parser = argparse.ArgumentParser(description='Convert all supported files from binary to text format')
parser.add_argument('folder', type=str, help='deploy folder')
parser.add_argument('output', type=str, help='output folder', default='-', nargs='?')
args = parser.parse_args()

input_folder = args.folder
output_folder = args.output
if output_folder == '-':
    output_folder = input_folder


print('Searching for files...')

filepaths = []
for root, dirnames, filenames in os.walk(input_folder):
    for filename in filenames:
        if filename.endswith('.inibin') or filename.endswith('.troybin'): #or filename.endswith('.luaobj'):
            filepath = os.path.join(root, filename)
            filepaths.append(filepath)

def process_file(infilepath: str):
    outfilepath = infilepath.replace(input_folder, output_folder, 1)
    outfilepath = re.sub(r'(bin|obj)$', '', outfilepath)
    #print(infilepath, '->', outfilepath)
    with open(infilepath, 'rb') as infile, open(outfilepath, 'w') as outfile:
        try:
            if infilepath.endswith('.inibin'):
                inibin2ini(infile, outfile)
            elif infilepath.endswith('.troybin'):
                troybin2troy(infile, outfile)
            #elif infilepath.endswith('.luaobj'):
            #    luaobj2lua(infile, outfile)
        except Exception as e:
            print(infilepath, e, sep='\n')
            traceback.print_exc()

process_map(process_file, filepaths, max_workers=1000, chunksize=10)
#list(map(process_file, filepaths))