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
            0x69: self.adc_, 0x65: self.adc_, 0x75: self.adc_, 0x6D: self.adc_, 0x7D: self.adc_, 0x79: self.adc_, 0x61: self.adc_, 0x71: self.adc_,
            0x29: self.and_, 0x25: self.and_, 0x35: self.and_, 0x2D: self.and_, 0x3D: self.and_, 0x39: self.and_, 0x21: self.and_, 0x31: self.and_,
            0x0A: self.asl_, 0x06: self.asl_, 0x16: self.asl_, 0x0E: self.asl_, 0x1E: self.asl_,
            0x24: self.bit_, 0x2C: self.bit_,
        }
        self.statbits = {
            "n": 0x80, "v": 0x40, "-": 0x20, "b": 0x10,
            "d": 0x08, "i": 0x04, "z": 0x02, "c": 0x01,
        }
        self.addrmodes = {
            0x69: self.imd, 0x65: self.zp, 0x75: self.zpix, 0x6D: self.abslt, 0x7D: self.absix, 0x79: self.absiy, 0x61: self.indix, 0x71: self.indiy,
            0x29: self.imd, 0x25: self.zp, 0x35: self.zpix, 0x2D: self.abslt, 0x3D: self.absix, 0x39: self.absiy, 0x21: self.indix, 0x31: self.indiy,
            0x0A: self.acc, 0x06: self.zp_, 0x16: self.zpix_, 0x0E: self.abs_, 0x1E: self.absix_,
            0x24: self.zp, 0x2C: self.abslt,
        }
        self.numbytes = {
            0x69: 2, 0x65: 2, 0x75: 2, 0x6D: 3, 0x7D: 3, 0x79: 3, 0x61: 2, 0x71: 2, # ADC
            0x29: 2, 0x25: 2, 0x35: 2, 0x2D: 3, 0x3D: 3, 0x39: 3, 0x21: 2, 0x31: 2, # AND
            0x0A: 1, 0x06: 2, 0x16: 2, 0x0E: 3, 0x1E: 3,                            # ASL
            0x24: 2, 0x2C: 3,
        }
        self.numops = {
            0x69: 1, 0x65: 1, 0x75: 1, 0x6D: 2, 0x7D: 2, 0x79: 2, 0x61: 1, 0x71: 1,
            0x29: 1, 0x25: 1, 0x35: 1, 0x2D: 2, 0x3D: 2, 0x39: 2, 0x21: 1, 0x31: 1, 
            0x0A: 0, 0x06: 1, 0x16: 1, 0x0E: 2, 0x1E: 2,
            0x24: 1, 0x2C: 2,
        }
    def imd(self, op1, op2, code):
        self.value = op1
    def zp(self, op1, op2, code):
        self.value = self.mem[op1]
    def zpix_(self, op1, op2, code):
        self.value = op1
    def zpix(self, op1, op2, code):
        self.value = self.mem[(op1 + self.x) % 0x100]
    def zpix_(self, op1, op2, code):
        self.value = op1 + self.x
    def zpiy(self, op1, op2, code):
        self.value = self.mem[(op1 + self.y) % 0x100]
    def zpiy_(self, op1, op2, code):
        self.value = op1
    def abslt(self, op1, op2, code):
        self.value = self.mem[op1 + 256*op2]
    def abslt_(self, op1, op2, code):
        op1 + 256*op2
    def absix(self, op1, op2, code):
        self.value = self.mem[op1 + 256*op2 + self.x]
    def absix_(self, op1, op2, code):
        op1 + 256*op2 + self.x
    def absiy(self, op1, op2, code):
        self.value = self.mem[op1 + 256*op2 + self.y]
    def absiy_(self, op1, op2, code):
        op1 + 256*op2 + self.y
    def rel(self, op1, op2, code):
        if op1 > 0x7f:
            self.val2 = ((self.pc+2 + op1 - 256) % 0x10000) // 0x100
            self.value = ((self.pc+2 + op1 - 256) % 0x10000) % 0x100
        else:  
            self.val2 = ((self.pc+2 + op1) % 0x10000) // 0x100
            self.value = ((self.pc+2 + op1) % 0x10000) % 0x100
    def indir(self, op1, op2, code):
        self.value = self.mem[op1 + 256*op2]
        self.val2 = self.mem[op1 + 256*op2 + 1]
    def indix(self, op1, op2, code):
        self.value = self.mem[op1 + self.x]
        self.val2 = self.mem[op1 + self.x + 1]
    def indiy(self, op1, op2, code):
        self.value = self.mem[op1] + self.y
        self.val2 = self.mem[op1 + 1] + self.y
    def acc(self, op1, op2, code):
        self.value = self.a
    def implied(self, op1, op2, code):
        pass
    def flag(self, flag, bitset=False, bitclear=False):
        if bitset:
            self.stat |= self.statbits[flag.lower()]
        if bitclear:
            self.stat &= ~(self.statbits[flag.lower()])
    def adc_(self, op1):
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
    def and_(self, op1):
        self.a &= op1
        if self.a == 0:
            self.flag("Z", bitset=True)
        else:
            self.flag("Z", bitclear=True)
            
        if self.a & 0x80:
            self.flag("N", bitset=True)
        else:
            self.flag("N", bitclear=True)
    def asl_(self, op1, op2, code):
        if code == 0x0A:
            self.a <<1
            self.a %= 0x100
        else:
            self.mem[op1 + 256*op2] <<= 1
            self.mem[op1 + 256*op2] %= 0x100
    # Next: BCC, BCS, and BEQ
    def bit_(self, op1, op2, code):
        if self.a & (self.value + 256+self.val2) == 0x00:
            self.flag("Z", bitset=True)
        else:  
            self.flag("Z", bitclear=True)
        if self.value & 0x80:
            self.flag("N", bitset=True)
        else:  
            self.flag("N", bitclear=True)
        if self.value & 0x40:
            self.flag("V", bitset=True)
        else:  
            self.flag("V", bitclear=True)
    def executeinst(self):
        self.curr = self.mem[self.pc]
        self.next = self.mem[self.pc+1]
        self.next2 = self.mem[self.pc+2]
        self.addrmodes[self.curr](self.next, self.next2, self.curr)
        if self.numops[self.curr] == 2:
            self.mnem[self.curr](self.value, self.val2)
        elif self.numbytes[self.curr] == 1:
            self.mnem[self.curr](self.value)
        elif self.numbytes[self.curr] == 0:
            self.mnem[self.curr]()
cpu = CPU()
# ADC AND ASL BCC BCS BEQ BIT BMI BNE BPL BRK BVC BVS CLC
# ✓   ✓   ✓   NXT NXT NXT ✓
# CLD CLI CLV CMP CPX CPY DEC DEX DEY EOR INC INX INY JMP
#
# JSR LDA LDX LDY LSR NOP ORA PHA PHP PLA PLP ROL ROR RTI
#
# RTS SBD SEC SED SEI STA STX STY TAX TAY TSX TXA TXS TYA
#
