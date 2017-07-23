#!/usr/bin/env python

import struct

crazyHashes = []

with open('crazyHashesFull', 'rb') as fp:
    try:
        while True:
            data = struct.unpack('I', fp.read(4))[0]
            crazyHashes.append(data)
    except:
        print "done reading"

crazyHashesEven = crazyHashes[0::2]
crazyHashesOdd = crazyHashes[1::2]

winBuff = []
iv84 = 0x84222325
ivCB = 0xCBF29CE4
hx1B3 = 0x1B3
hx100 = 0x100
index = 0

for i in range(len(crazyHashesEven)):
    for aChar in range(0x20, 0x7F):
        eax = ((aChar^iv84) * hx1B3) & 0xFFFFFFFF
        edx = (((ivCB*hx1B3) & 0xFFFFFFFF) + (((aChar^iv84) * 0x100) & 0xFFFFFFFF) & 0xFFFFFFFF)
        edx += ((aChar^iv84)*hx1B3 & 0xFFFFFFFF00000000) >> 32
        if eax == crazyHashesEven[index] and edx == crazyHashesOdd[index]:
            winBuff.append(aChar)
    index += 1
    
print ''.join(map(chr, winBuff))
