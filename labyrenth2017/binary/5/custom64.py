#!/usr/bin/env python

# modified from https://github.com/xamiel/custombase64/blob/master/custombase64.py 

import base64
import string
import random

cuscharset = "PANDEFGHIJKLMCOBQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
b64charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

encodedset = string.maketrans(b64charset, cuscharset)
decodedset = string.maketrans(cuscharset, b64charset)


def dataencode(x):
    y = base64.b64encode(x)
    y = y.translate(encodedset)
    return y


def datadecode(x):
    y = x.translate(decodedset)
    y = base64.b64decode(y)
    return y


#plaintext = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNN"

#  Encode the plaintext string
#enc = dataencode(plaintext)
enc = "UEFOREEgUEFOREEgUEFOREEhIEJAU0U2CNAQQU5EQSAGTlY2CNAQQU5EQSAYT1IgUEFOREE="
#  Decode back into plaintext string
dec = datadecode(enc)

print enc
print dec
