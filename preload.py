import re
RE_PART = re.compile("\\{Function=BBPreloadParticle, Params=\\{Name=\"(.+)\"")
RE_SPELL = re.compile("\\{Function=BBPreloadSpell, Params=\\{Name=\"(.+)\"")
RE_CHAR = re.compile("\\{Function=BBPreloadCharacter, Params=\\{Name=\"(.+)\"")

def read(buffer):
    data = buffer.read().decode('utf-8')
    return {
        "Part": [ part.group(1).lower() for part in RE_PART.finditer(data) ],
        "Spell": [ spell.group(1).lower() for spell in RE_SPELL.finditer(data) ],
        "Char": [ char.group(1).lower() for char in RE_CHAR.finditer(data) ]
    }
def from_file(name):
    file = open(name, 'rb')
    return read(file)
