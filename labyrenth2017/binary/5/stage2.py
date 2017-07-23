#!/usr/bin/env python

targetChars = [0x4A, 0x5C, 0x57, 0x5A, 0x5A]

for target in targetChars:
    for x in range(0x20, 0x7F):
        if x^(x/2) == target:
            print "Target: %s - X: - %s" % (chr(target), chr(x))
