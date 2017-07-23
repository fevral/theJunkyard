#!/usr/bin/env python

import sys

def tryKey(key):

    basicBlock = []
    
    rollingSum = 0
    keyLen = 0xC

    for i in range(0x100):
        basicBlock.append(i)
    
    for j in range(0x100):
        rollingSum = (rollingSum + (ord(key[j%keyLen]) + basicBlock[j])) & 0xFF
        basicBlock[j], basicBlock[rollingSum] = basicBlock[rollingSum], basicBlock[j]
    return basicBlock

def crypt(whichBlock, a, b):

    inputFile = bytearray((open(sys.argv[1], 'rb').read()))
    swapped256 = bytearray(whichBlock)
    counter0 = 0
    counter1 = 0
    encryptedFile = inputFile
    swapValList = []
    for index in range(len(inputFile)):
    
        counter0 = (counter0 + 1) & 0xFF
        counter1 = (counter1 + swapped256[counter0]) & 0xFF
        swapped256[counter0], swapped256[counter1] = swapped256[counter1], swapped256[counter0]
        sumOfSwappyVals = (swapped256[counter0] + swapped256[counter1]) & 0xFF
        swapValList.append(sumOfSwappyVals)
        encryptedFile[index] = inputFile[index] ^ swapped256[sumOfSwappyVals]
        
    open('crypt-a-' + str(a) + '-b-' + str(b), 'wb').write(str(encryptedFile))
    return 0
print "==============Crypt=============="
alphaBits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
for a in alphaBits:
    for b in alphaBits:
        key = ['0','0','1','c','4','2','9','2','d','f', a, b]
        crypt(tryKey(key), a, b)

