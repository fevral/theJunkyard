#!/usr/bin/env python


xorConst  = 0x811C9DC5
imulConst = 0x1000193

winChars = []

def calcAbyte(target):

    for c in range(0x20, 0x7F):
        calced = (((c ^ xorConst) & 0xFFFFFFFF) * imulConst) & 0xFFFFFFFF
        if calced == target:
            winChars.append(c)

    return c

targetHashes = [0xE60C2C52, 0xEA0C329E, 0xE10C2473, 0xE00C22E0]

for target in targetHashes:
    calcAbyte(target)

print ''.join(map(chr, winChars))
print map(hex, winChars)
