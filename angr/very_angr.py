#!/usr/bin/env python
import angr


# load the binary
b = angr.Project("very_success.exe", load_options={"auto_load_libs":False})

# create a blank_state (https://github.com/angr/angr-doc/blob/master/docs/toplevel.md#the-factory) at the top of the flag checking function
s = b.factory.blank_state(addr=0x401084)

# Since we started inside this function, we have to set up the args that were pushed on to the stack from the previous function
# ...0 sounds like a good place to store memory, why not? So esp+4 (arg0) shall be found at 0
s.mem[s.regs.esp+4:].dword = 0
s.mem[s.regs.esp+8:].dword = 100
s.mem[s.regs.esp+0xC:].dword = 200

# let's store a symbolic BitVector (https://github.com/angr/angr-doc/blob/master/docs/claripy.md#claripy-asts) large enough (0x28 * 8 bits) for the proper input (based on the loop exit conditions at 0x40128F
magicLen = 0x25
magicBytes = open('magicBytes', 'rb').read()

s.memory.store(0, s.se.BVV(magicBytes))
s.memory.store(100, s.se.BVS("guess", magicLen*8))
s.memory.store(200, s.se.BVV(magicLen, 32))


# instantiate a path_group (https://github.com/angr/angr-doc/blob/master/docs/pathgroups.md)
pg = b.factory.path_group(s)

# ask them to explore until they find the winning basic block
pg.explore(find=0x4010d5, avoid=0x4010d7)


# for those paths which have found a way to the desired address...let's examine their state
for found in pg.found:
    # specifically, let's see what string is in memory at 100 for successful paths
    print found.state.se.any_str(found.state.memory.load(100, 0x25)).strip('\0')
