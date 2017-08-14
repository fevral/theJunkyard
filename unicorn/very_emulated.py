#!/usr/bin/env python

# lots of good help from these awesome scripts/examples/blogs

#https://github.com/unicorn-engine/unicorn/blob/master/bindings/python/sample_x86.py#L24
#https://r3v3rs3r.wordpress.com/2015/12/12/unicorn-vs-malware/
#https://github.com/karttoon/shellbug
#https://github.com/unicorn-engine/unicorn/issues/451

from unicorn import *
from unicorn.x86_const import *

# taking a lazy approach to automation and wrapping the entire thing in a loop

rightChars = 0

# dummy string to guess with
guessString = list("!" * 0x25)

# and setting our win state
foundIt = False

while not foundIt:

    for c in xrange(0x20, 0x7F):
        guessString[rightChars] = chr(c)

        # creating a custom hook for every instruction that executes
        # a brutish approach, but it'll work
        def hook_code(uc, address, size, user_data):
            global rightChars
            global foundIt

            # if we have already executed the cmovne cx, dx, and cx is zero...
            # then this input is bad and we need to try a different one
            # :> ? 0x4010cd - 0x401084
            # 73 0x49 0111 73 0000:0049 73 "I" 01001001 73.0 73.000000f 73.000000
        
            if address == 0x49:
                ecx = uc.reg_read(UC_X86_REG_ECX)
                # we got hit with the cmovne, it was a bad guess
                if ecx == 0:
                    mu.emu_stop()
                # we managed to loop all the way to the last character...we won
                elif ecx == 1:
                    foundIt = True
                    mu.emu_stop()
                # if loop count and number of characters we already found match, we move on
                elif ecx == 0x25 - rightChars:
                    #print ("Found One!")
                    #print (uc.mem_read(guessAddress+rightChars, 1))
                    rightChars += 1
            
        # spawn a unicorn thing
        mu = Uc(UC_ARCH_X86, UC_MODE_32)
        
        # some generic addresses for our emulation
        baseAddress = 0
        STACK_ADDRESS = 0xffff000
        STACK_SIZE = 0x1000
        
        # function code
        functionCode = "\x55\x89\xe5\x83\xec\x00\x57\x56\x31\xdb\xb9\x25\x00\x00\x00\x39\x4d\x10\x7c\x3f\x8b\x75\x0c\x8b\x7d\x08\x8d\x7c\x0f\xff\x66\x89\xda\x66\x83\xe2\x03\x66\xb8\xc7\x01\x50\x9e\xac\x9c\x32\x44\x24\x04\x86\xca\xd2\xc4\x9d\x10\xe0\x86\xca\x31\xd2\x25\xff\x00\x00\x00\x66\x01\xc3\xae\x66\x0f\x45\xca\x58\xe3\x07\x83\xef\x02\xe2\xcd\xeb\x02\x31\xc0\x5e\x5f\x89\xec\x5d\xc3"
        
        magicBytes = "\xaf\xaa\xad\xeb\xae\xaa\xec\xa4\xba\xaf\xae\xaa\x8a\xc0\xa7\xb0\xbc\x9a\xba\xa5\xa5\xba\xaf\xb8\x9d\xb8\xf9\xae\x9d\xab\xb4\xbc\xb6\xb3\x90\x9a\xa8"
        
        # map 0x1000  bytes at baseAddress
        mu.mem_map(baseAddress, 0x1000)
        mu.mem_map(STACK_ADDRESS, STACK_SIZE)
        
        # set our ESP with some room for the previous args to this function
        mu.reg_write(UC_X86_REG_ESP, STACK_ADDRESS + STACK_SIZE - 0x10)
        
        # address where we want to write the magicBytes
        magicBytesAddress = 0x200
        
        # write them
        mu.mem_write(magicBytesAddress, magicBytes)
        
        # address where we want to write our input buffer
        guessAddress = 0x300
        
        # write it
        mu.mem_write(guessAddress, ''.join(guessString))
        
        # address where we want to write the magicLen (input length value we discovered)
        magicLenAddress = 0x400
        
        # its value 
        magicLen = 0x25
        
        # write it
        mu.mem_write(magicLenAddress, str(magicLen))
        
        # "push" our args onto the stack (the addresses of our buffers of interest)
        mu.mem_write(STACK_ADDRESS+STACK_SIZE-0xc, "\x00\x02\x00\x00")
        mu.mem_write(STACK_ADDRESS+STACK_SIZE-8,   "\x00\x03\x00\x00")
        mu.mem_write(STACK_ADDRESS+STACK_SIZE-4,   "\x00\x04\x00\x00")
        
        # write the function code at the base address
        mu.mem_write(baseAddress, functionCode)
        
        # hook every instruction, because it'll work
        mu.hook_add(UC_HOOK_CODE, hook_code)
        
        # start the brute
        try:
            mu.emu_start(baseAddress, baseAddress + len(functionCode))
            if foundIt:
                print ''.join(guessString)
                break
        except UcError as e:
            print "Error: %s" % e

