#!/usr/bin/env python
import angr

b = angr.Project("AntiD_clean.exe", load_options={"auto_load_libs":False})
s = b.factory.blank_state(addr=0x11411B0)

s.mem[s.regs.esp+4:].dword = 0

s.memory.store(0, s.se.BVS("ans", 0x28*8))

pg = b.factory.path_group(s)
pg.explore(find=0x114135D)
for found in pg.found:
    print found.state.se.any_str(found.state.memory.load(0, 0x28)).strip('\0')
