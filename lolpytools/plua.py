import struct
import io
import re
import os

def read(buffer):
    def readx(count):
        return buffer.read(count)
    def read_none():
        return None
    def read_bool():
        return struct.unpack_from('<?', readx(1))[0]
    def read_byte():
        return struct.unpack_from('<B', readx(1))[0]
    def read_int():
        return struct.unpack_from('<i', readx(4))[0]
    def read_size():
        return struct.unpack_from('<I', readx(4))[0]
    def read_num():
        return struct.unpack_from('<d', readx(8))[0]
    def read_str():
        size = read_size()
        data = struct.unpack_from(str(size)+'s', readx(size))[0]
        return data[:-1].decode('utf-8')
    def read_op():
        return struct.unpack_from('I', readx(4))[0]
    read_const_map = [read_none, read_bool, None, read_num, read_str]
    def read_const():
        const_type = read_byte()
        return read_const_map[const_type]()
    def read_list(what):
        return [what() for c in range(0, read_int())]
        
    magic = readx(12)
    if not magic == b'\x1B\x4C\x75\x61\x51\x00\x01\x04\x04\x04\x08\x00':
        raise "Magic doesn't match"
    source = read_str()
    flags = readx(12)
    ops = read_list(read_op)
    consts = read_list(read_const)
    regs = [[None] for x in range(0, 256)]
    G = {}
    pc = 0
    def R(r):
        return regs[r]
    def K(k):
        return [consts[k]]
    def RK(rk):
        return K(rk & 0xFF) if rk > 0xFF else R(rk)
    def F8(v):
        x = v & 0b111
        e = v >> 3
        return x if e == 0 else (x | 8) * (2 ** (e -1))
    while True:
        if pc >= len(ops):
            raise "Pc out of range!"
        code = ops[pc]
        pc = pc + 1
        op = code & 0b111111
        a = (code >> 6) & 0b11111111
        c = (code >> 14) & 0b111111111
        b = (code >> 23) & 0b111111111
        bx = (code >> 14) & 0b111111111111111111
        sbx = bx - 131071
        # 0 MOVE
        if op == 0:
            R(a)[0] = R(b)[0]
        # 1 LOADK
        elif op == 1:
            R(a)[0] = K(bx)[0]
        # 2 LOADBOOL
        elif op == 2:
            R(a)[0] = not b == 0
            if not c == 0:
                pc = pc + 1
        # 3 LOADNIL
        elif op == 3:
            for r in range(a, b + 1):
                R(r)[0] = None
        # 5 GETGLOBAL Read a global variable into a register
        elif op == 5:
            index = K(bx)[0]
            value = G[index] if index in G else index
            R(a)[0] = value
        # 6 GETTABLE Read a table element into a register
        elif op == 6:
            table = R(b)[0]
            index = R(c)[0]
            if isinstance(index, str):
                table = table[0]
            value = table[index] if index in table else None
            R(a)[0] = value
        # 7 SETGLOBAL Write a register value into a global variable
        elif op == 7:
            index = K(bx)[0]
            value = R(a)[0]
            G[index] = value
        # 9 SETTABLE Write a register value into a table element
        elif op == 9:
            table = R(a)[0]
            index = RK(b)[0]
            value = RK(c)[0]
            if isinstance(index, str):
                table = table[0]
            table[index] = value
        #10 NEWTABLE Create a new table
        elif op == 10:
            n = F8(b)
            m = F8(c)
            value = [{}] + [None for x in range(0, n)]
            R(a)[0] = value
        #28 CALL Call a closure
        elif op == 28:
            pass
        #30 RETURN Return from function call
        elif op == 30:
            break
        #34 SETLIST Set a range of array elements for a table
        elif op == 34:
            table = R(a)[0]
            fpf = 50
            for i in range(1, b + 1):
                value = R(a + i)[0]
                index = (c - 1) * fpf + i
                table[index] = value
        #36 CLOSURE Create a closure of a function prototype
        elif op == 36:
            R(a)[0] = "<CLOUSURE>"
            pc = pc + 1
        else:
            raise "Unknown opcode: {}".format(op)
    return {
        "Values": G
    }

def from_file(name):
    with open(name, 'rb') as file:
        return read(file)

