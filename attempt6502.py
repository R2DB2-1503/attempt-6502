class CPU:
    def __init__(self):
        self.a = 0x00
        self.x = 0x00
        self.y = 0x00
        self.pc = 0x8000
        self.sp = 0xFF
        self.stat = 0b00100000
        self.mem = [0x00] * 65536
        self.curr = 0x00
        self.next = 0x00
        self.next2 = 0x00
        self.value = 0x00
        self.val2 = 0x00
        self.mnem = {
            0x69: self.adc,
            0x65: self.adc,
            0x75: self.adc,
            0x6D: self.adc,
            0x7D: self.adc,
            0x79: self.adc,
            0x61: self.adc,
            0x71: self.adc,
        }
        self.statbits = {
            "n": 0x80,
            "v": 0x40,
            "-": 0x20,
            "b": 0x10,
            "d": 0x08,
            "i": 0x04,
            "z": 0x02,
            "c": 0x01,
        }
        self.addrmodes = {
            0x69: self.imd,
            0x65: self.zp,
            0x75: self.zpix,
            0x6D: self.abslt,
            0x7D: self.absix,
            0x79: self.absiy,
            0x61: self.indix,
            0x71: self.indiy,
        }
        self.numbytes = {
            0x69: 2,
            0x65: 2,
            0x75: 2,
            0x6D: 3,
            0x7D: 3,
            0x79: 3,
            0x61: 2,
            0x71: 2,
        }
        self.numops = {
            0x69: 1,
            0x65: 1,
            0x75: 1,
            0x6D: 2,
            0x7D: 2,
            0x79: 2,
            0x61: 1,
            0x71: 1,
        }
    def imd(self, op1, op2):
        self.value = op1
    def zp(self, op1, op2):
        self.value = self.mem[op1]
    def zpix(self, op1, op2):
        self.value = self.mem[(op1 + self.x) % 0x100]
    def zpiy(self, op1, op2):
        self.value = self.mem[(op1 + self.y) % 0x100]
    def abslt(self, op1, op2):
        self.value = self.mem[op1 + 256*op2]
    def absix(self, op1, op2):
        self.value = self.mem[op1 + 256*op2 + self.x]
    def absiy(self, op1, op2):
        self.value = self.mem[op1 + 256*op2 + self.x]
    def rel(self, op1, op2):
        if op1 > 0x7f:
            self.val2 = ((self.pc+2 + op1 - 256) % 0x10000) // 0x100
            self.value = ((self.pc+2 + op1 - 256) % 0x10000) % 0x100
        else:  
            self.val2 = ((self.pc+2 + op1) % 0x10000) // 0x100
            self.value = ((self.pc+2 + op1) % 0x10000) % 0x100
    def indir(self, op1, op2):
        self.value = self.mem[op1 + 256*op2]
        self.val2 = self.mem[op1 + 256*op2 + 1]
    def indix(self, op1, op2):
        self.value = self.mem[op1 + self.x]
        self.val2 = self.mem[op1 + self.x + 1]
    def indiy(self, op1, op2):
        self.value = self.mem[op1] + self.y
        self.val2 = self.mem[op1 + 1] + self.y
    def accumulator(self, op1, op2):
        self.value = self.a
    def implied(self, op1, op2):
        pass
    def flag(self, flag, bitset=False, bitclear=False):
        if bitset:
            self.stat |= self.statbits[flag.lower()]
        if bitclear:
            self.stat &= ~(self.statbits[flag.lower()])
    def adc(self, op1):
        w = op1
        if self.a + op1 > 0xff:
            flag("C", bitset=True)
            w -= 0x100
        else:
            flag("C", bitclear=True)  
        self.a += w
        if ((self.a ^ result) & (op1 ^ result) & 0x80):
            self.flag("V", bitset=True)
        else:
            self.flag("V", bitclear=True)
        if self.a == 0:
            self.flag("Z", bitset=True)
        else:
            self.flag("Z", bitclear=True)
            
        if self.a & 0x80:
            self.flag("N", bitset=True)
        else:
            self.flag("N", bitclear=True)
    # Next: AND
    def executeinst(self):
        self.curr = self.mem[pc]
        self.next = self.mem[pc+1]
        self.next2 = self.mem[pc+2]
        self.addrmodes[self.curr](self.next, self.next2)
        if self.numops[self.curr] == 2:
            self.mnem[self.curr](self.value, self.val2)
        elif self.numbytes[self.curr] == 1:
            self.mnem[self.curr](self.value)
        elif self.numbytes[self.curr] == 0:
            self.mnem[self.curr]()
# ADC AND ASL BCC BCS BEQ BIT BMI BNE BPL BRK BVC BVS CLC
# √   
# CLD CLI CLV CMP CPX CPY DEC DEX DEY EOR INC INX INY JMP
#
# JSR LDA LDX LDY LSR NOP ORA PHA PHP PLA PLP ROL ROR RTI
#
# RTS SBD SEC SED SEI STA STX STY TAX TAY TSX TXA TXS TYA
#