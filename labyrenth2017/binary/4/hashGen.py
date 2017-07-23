#!/usr/bin/env python

constArray = bytearray(open('constArray', 'rb').read())

mac = [8,0,0x27,0xa1,0xef,0xb9]
new5 = [0,0,0,0,0]

for outer in range(5):
    for inner in range(5):
        new5[outer] = new5[outer] + (constArray[(inner*20 + outer*4)] * mac[inner])
    new5[outer] %= 0xFB


guess = [new5[0],0,0,0,new5[1],0,0,0,new5[2],0,0,0,new5[3],0,0,0,new5[4],0,0,0]
print map(chr, guess)
