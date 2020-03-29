import re
import json
RE_TR = re.compile('\\s*tr\\s*\\"(.*)\\"\\s*=\\s*\\"(.*)\\"\\s*')
# reads fontconfig from binary buffer
def read(buffer):
    data = buffer.read().decode('utf-8-sig')
    target = { t.group(1) : t.group(2) for t in RE_TR.finditer(data) }
    return {
        "MetaData": {
            "ContentFormatVersion": 4,
            "Id": "",
            "Name": "",
            "ResourcePath": "",
            "Format": "fontconfig"
        },
        "Values": target
    }
# reads fontconfig from file in filesystem
def from_file(name):
    file = open(name, 'rb')
    return read(file)

def to_json(data):
    return json.dumps(data, indent=2)
