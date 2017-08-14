#!/usr/bin/env python

from __future__ import print_function
from unicorn import *
from unicorn.x86_const import *
import binascii

# don't need much space probably...
ADDRESS = 0x10000

# the bytes of the shellcode decrypt function
CODE = "\x33\xDB\x0F\x1F\x40\x00\xB8\xAB\xAA\xAA\xAA\xF7\xE3\x8B\xC3\xC1\xEA\x02\x8D\x0C\x52\x03\xC9\x2B\xC1\x74\x04\x80\x34\x33\x78\xF6\xC3\x03\x74\x04\x80\x34\x33\x65\xF6\xC3\x01\x74\x04\x80\x34\x33\x64\x80\x34\x33\x6E\x43\x81\xFB\xD0\x04\x00\x00\x7C\xC8\x8D\x85\xE0\xFC\xFF\xFF\x50\xFF\xD6\x83\xF8\x01"

try:

    # initialize unicorn with Uc object
    mu = Uc(UC_ARCH_X86, UC_MODE_32)
    
    # always got map memory before emulation
    mu.mem_map(ADDRESS, 4096)
    
    # write the shellcode decrypt function bytes to our base address
    mu.mem_write(ADDRESS, CODE)
    
    # ok, code is written there, but we need to fix the state...there were important
    # things in the registers...and memory...namely, pointer to the encrypted shellcode
    # and the shellcode itself
    
    # address of the encrypted shellcode
    shellADDRESS = 0x1000
    
    # map it! we know from static analysis it is only 0x4D0 bytes, but whatever...
    # we're feeling generous and we take our personal space pretty seriously
    mu.mem_map(shellADDRESS, 4096)
    
    # and now we write the encrypted shellcode there
    encryptedSCbytes = open('1.bin', 'rb').read()
    mu.mem_write(shellADDRESS, encryptedSCbytes)
    
    
    # fix the registers...they're taken care of largely by the code, just need to set esi
    mu.reg_write(UC_X86_REG_ESI, shellADDRESS)
    
    # ok...should be ready to emulate
    # -5 so that we don't end up executing the call esi, and the cmp eax, 0x1, or even grabbing the arg
    # we just want the decrypted shellcode
    mu.emu_start(ADDRESS, ADDRESS + len(CODE) - 12)
    
    decryptedSCbytes = mu.mem_read(shellADDRESS, 0x4D0)
    # print (binascii.hexlify(decryptedSCbytes))
    # bonus round...we'll disassemble the shellcode with capstone!
    from capstone import *
    
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    for i in md.disasm(str(decryptedSCbytes), 0):
        print("0x%x:\t%s\t%s" % (i.address, i.mnemonic, i.op_str))
    
    # write the decrypted shellcode to a file
    open('shell.out', 'wb').write(str(decryptedSCbytes))
    
    print (binascii.hexlify(decryptedSCbytes))
    
    
    
    # having examined this thing in x64dbg, we the next code of interest is
    # the decryption of stage 2
    # from x64dbg, malloc returned a pointer to 0x7E1FD8
    # and the decryption loop gets set up at 0x7E223D
    # difference of 0x265
    
    # new shellcode emu
    CODE2 = str(decryptedSCbytes[0x265:0x265+0x2D])
    ADD2 = 0x20000
    
    # map it
    mu.mem_map(ADD2, 4096)
    
    # write it
    mu.mem_write(ADD2, CODE2)
    
    # stage 2 encrypted map and write
    
    shellADD2 = 0x2000
    mu.mem_map(shellADD2, 4096)
    encrypted2 = open('2.bin', 'rb').read()
    mu.mem_write(shellADD2, encrypted2)
    
    
    # set the regs, really just have to make sure that ESI is  char *pass
    # and EDI void *shell2
    mu.reg_write(UC_X86_REG_EDI, shellADD2)
    
    # need to write the char * pass
    passAddr = shellADD2 + 0x500
    mu.mem_write(passAddr, "Labyshellcode$1\x00")  # provide correct pass for testing
    
    mu.reg_write(UC_X86_REG_ESI, passAddr)
    
    # emu2? loop is only 0x2D bytes
    mu.emu_start(ADD2, ADD2+0x2D)
    
    decrypted2 = mu.mem_read(shellADD2, 0x480)
    print (binascii.hexlify(decrypted2))
    
    
    # decrypt 3!
    CODE3 = str(decrypted2[0x207:0x207+0x35])
    ADD3 = 0x30000
    
    mu.mem_map(ADD3, 4096)
    mu.mem_write(ADD3, CODE3)
    
    shellADD3 = 0x3000
    mu.mem_map(shellADD3, 4096)
    encrypted3 = open('3.bin', 'rb').read()
    mu.mem_write(shellADD3, encrypted3)
    
    mu.reg_write(UC_X86_REG_EDI, shellADD3)
    mu.reg_write(UC_X86_REG_ESI, passAddr)
    mu.emu_start(ADD3, ADD3+0x35)
    
    decrypted3 = mu.mem_read(shellADD3, 0x2B0)
    print (binascii.hexlify(decrypted3))
    
    
    # solve checksum, address of shellADD3 + offset to checksum function
    CHECKSUMMER = str(decrypted3[0x3200:0x3200+0xAD])
    ADDCHECK = 0x3200
    stackADDR = 0x3800 # just somewhere out of the way
    winningSum = 0xeac016eb
    
    # find the mystery char
    for ch in range (0x20, 0x7F):
        mu.mem_write(stackADDR, chr(ch))   # write the correct value, for testing
        mu.reg_write(UC_X86_REG_ECX, stackADDR)
        mu.emu_start(ADDCHECK, ADDCHECK+0xAD)
        thisSum = mu.reg_read(UC_X86_REG_EAX)
        if thisSum == winningSum:
            print ("The mystery char is: %s" % chr(ch))
    
except UcError as e:
    print ("Error: %s" % e)
