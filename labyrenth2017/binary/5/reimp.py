#!/usr/bin/env python

import sys
sys.setrecursionlimit(1000000000)
someBuff = []
theVars = [0x1A6D, 0, 0x6197ECB, 0, 0x9DE8D6D, 0, 0xBDD96882, 0, 0x148ADD, 0, 0x9DE8D6D, 0, 0xBDD96882, 0, 0x148ADD, 0, 0x29CEA5DD, 0, 0x35C7E2, 0, 0x5704E7, 0, 0x15A419A2, 0, 0x6D73E55F, 0, 0x35C7E2, 0, 0x8CCCC9, 0, 0x8CCCC9, 0, 0x9DE8D6D, 0]

theVarsEven = theVars[0::2]
theVarsOdd = theVars[1::2]
for i in range (0x4000):
    someBuff.append(0)


def recursy(moddedIndex, tryBuff, someSize):
    if moddedIndex == 0:
        return 0
    elif moddedIndex == 1:
        return moddedIndex
    else:
        tryBuff[moddedIndex]
        if tryBuff[moddedIndex] != 0:
            return tryBuff[moddedIndex]
        redi = recursy(moddedIndex - 2, tryBuff, 0x1000) & 0xFFFFFFFF
        redi = (redi + (recursy(moddedIndex -1, tryBuff, 0x1000) & 0xFFFFFFFF) & 0xFFFFFFFF)
        tryBuff[moddedIndex] = redi
        return redi

def tryOne(a, tryBuff, winCount):
    successFlag = 0
    modIndex = (a - 0x40) & 0xFF
    if modIndex == 0:
        edi = 0
    elif modIndex == 1:
        edi = modIndex
    else:
        edi = tryBuff[modIndex]
        if edi == 0:
            edi = recursy(modIndex - 2, tryBuff, 0x1000) & 0xFFFFFFFF
            edi = (edi + (recursy(modIndex -1, tryBuff, 0x1000) & 0xFFFFFFFF) & 0xFFFFFFFF)
            tryBuff[modIndex] = edi
            #print hex(someBuff[modIndex])
    eax = 0
    if edi == theVarsEven[winCount]:
        if eax == theVarsOdd[winCount]:
            successFlag = 1
    return successFlag, tryBuff

winCount = 0
newBuff = someBuff
winBuff = []
while winCount < 0x11:
    tryBuff = newBuff
    win = 0
    try:
        for aChar in range(0x20, 0x7F):
            win, newBuff = tryOne(aChar, tryBuff, winCount)
            if win:
                winBuff.append(aChar)
                winCount += 1 
    except:
        break
print ''.join(map(chr, winBuff))
