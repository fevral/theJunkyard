#!/usr/bin/env python

import md5

theMacs = []

theMacs.append("00A19B")
theMacs.append("001c42")
theMacs.append("001c14")
theMacs.append("000c29")
theMacs.append("005056")
theMacs.append("000569")
theMacs.append("000017")
theMacs.append("080027")
theMacs.append("080020")
theMacs.append("000F4B")
theMacs.append("0003BA")
theMacs.append("00007D")
theMacs.append("002128")
theMacs.append("0021F6")
theMacs.append("0010E0")
theMacs.append("00144F")
theMacs.append("001397")
theMacs.append("00A0A4")
theMacs.append("2CC260")
theMacs.append("00104F")
theMacs.append("000782")
theMacs.append("0020F2")
theMacs.append("00015D")

macBytes = []
for mac in theMacs:
    macByte = [mac[i:i+2] for i in range(0, len(mac), 2)]
    macBytes.append((ord(macByte[0].decode('hex'))))
    macBytes.append((ord(macByte[1].decode('hex'))))
    macBytes.append((ord(macByte[2].decode('hex'))))
constArray = bytearray(open('constArray', 'rb').read())

def ohMyGod(onceAgain):
    return macBytes[onceAgain*3+0], macBytes[onceAgain*3+1], macBytes[onceAgain*3+2]

def generateMacHash(c, a, b):

    here, i, go = ohMyGod(c)
    mac = [here, i, go, a, b, 0] # last 0 has no meaning, it is not used
    new5 = [0,0,0,0,0]

    for outer in range(5):
        for inner in range(5):
            new5[outer] = new5[outer] + (constArray[(inner*20 + outer*4)] * mac[inner])
        new5[outer] %= 0xFB
    return new5

winningPrefixes = []
for c in range(len(theMacs)):
    print "%d: %s" % (c, theMacs[c])
    for a in range(0x100):
        for b in range(0x100):
            idSeed = generateMacHash(c, a, b)
            guess = [idSeed[0],0,0,0,idSeed[1],0,0,0,idSeed[2],0,0,0,idSeed[3],0,0,0,idSeed[4],0,0,0,]
            guess = map(chr, guess)
            guessString = ''.join(guess)

            result = md5.new(guessString).hexdigest()

            #target = "2acac5be475f7f80d15c18c96465c54c"
            target = "da91e949f4c2e814f811fbadb3c195b8"
            if result == target:
                print "got it!"
                print "a: %s\nb: %s\n" % (hex(a), hex(b))
                winningPrefixes.append(c)

print winningPrefixes

