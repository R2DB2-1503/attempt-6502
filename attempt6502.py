import pygame, sys
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
            0xA9: self.lda_, 0xA5: self.lda_, 0xB5: self.lda_, 0xAD: self.lda_, 0xBD: self.lda_, 0xB9: self.lda_, 0xA1: self.lda_, 0xB1: self.lda_,
            0xA2: self.ldx_, 0xA6: self.ldx_, 0xB6: self.ldx_, 0xAE: self.ldx_, 0xBE: self.ldx_,
            0xA0: self.ldy_, 0xA6: self.ldy_, 0xB6: self.ldy_, 0xAC: self.ldy_, 0xBC: self.ldy_,
            0xE6: self.inc_ , 0xF6: self.inc_ , 0xEE: self.inc_ , 0xFE: self.inc_,
            0xC6: self.dec_, 0xD6: self.dec_, 0xCE: self.dec_, 0xDE: self.dec_,
            0xCA: self.dex_, 0xE8: self.inx_, 0x88: self.dey_, 0xC8: self.iny_,
            0x85: self.sta_, 0x95: self.sta_, 0x8D: self.sta_, 0x9D: self.sta_, 0x99: self.sta_, 0x81: self.sta_, 0x91: self.sta_,
            0x86: self.stx_, 0x96: self.stx_, 0x8E: self.stx_,
            0x84: self.stx_, 0x94: self.stx_, 0x8C: self.stx_,
            0xEA: self.nop_, 0xAA: self.tax_, 0x8A: self.txa_, 0xA8: self.tay_, 0x98: self.tya_, 0x9A: self.txs_, 0xBA: self.tsx_,
            
        }
        self.statbits = {
            "n": 0x80, "v": 0x40, "-": 0x20, "b": 0x10,
            "d": 0x08, "i": 0x04, "z": 0x02, "c": 0x01,
        }
        self.addrmodes = {
            0x69: self.imd, 0x65: self.zp, 0x75: self.zpix, 0x6D: self.abslt, 0x7D: self.absix, 0x79: self.absiy, 0x61: self.indix, 0x71: self.indiy,
            0x29: self.imd, 0x25: self.zp, 0x35: self.zpix, 0x2D: self.abslt, 0x3D: self.absix, 0x39: self.absiy, 0x21: self.indix, 0x31: self.indiy,
            0x0A: self.acc, 0x06: self.zp, 0x16: self.zpix_, 0x0E: self.abslt_, 0x1E: self.absix_,
            0x24: self.zp, 0x2C: self.abslt,
            0xA9: self.imd, 0xA5: self.zp, 0xB5: self.zpix, 0xAD: self.abslt, 0xBD: self.absix, 0xB9: self.absiy, 0xA1: self.indix, 0xB1: self.indiy,
            0xA2: self.imd, 0xA6: self.zp, 0xB6: self.zpix, 0xAE: self.abslt, 0xBE: self.absix,
            0xA0: self.imd, 0xA6: self.zp, 0xB6: self.zpix, 0xAC: self.abslt, 0xBC: self.absix,
            0xE6: self.zp, 0xF6: self.zpix, 0xEE: self.abslt, 0xFE: self.absix,
            0xC6: self.zp, 0xD6: self.zpix, 0xCE: self.abslt, 0xDE: self.absix,
            0xCA: self.impl, 0xE8: self.impl, 0x88: self.impl, 0xC8: self.impl,
            0x85: self.zp, 0x95: self.zpix, 0x8D: self.abslt, 0x9D: self.absix, 0x99: self.absiy, 0x81: self.indix, 0x91: self.indiy,
            0x86: self.zp, 0x96: self.zpiy, 0x8E: self.abslt,
            0x84: self.zp, 0x94: self.zpix, 0x8C: self.abslt,
            0xEA: self.impl, 0xAA: self.impl, 0x8A: self.impl, 0xA8: self.impl, 0x98: self.impl, 0x9A: self.impl, 0xBA: self.impl,
        }
        self.numbytes = {
            0x69: 2, 0x65: 2, 0x75: 2, 0x6D: 3, 0x7D: 3, 0x79: 3, 0x61: 2, 0x71: 2, # ADC
            0x29: 2, 0x25: 2, 0x35: 2, 0x2D: 3, 0x3D: 3, 0x39: 3, 0x21: 2, 0x31: 2, # AND
            0x0A: 1, 0x06: 2, 0x16: 2, 0x0E: 3, 0x1E: 3,                            # ASL
            0x24: 2, 0x2C: 3,
            0xA9: 2, 0xA5: 2, 0xB5: 2, 0xAD: 3, 0xBD: 3, 0xB9: 3, 0xA1: 2, 0xB1: 2,
            0xA2: 2, 0xA6: 2, 0xB6: 2, 0xAE: 3, 0xBE: 3,
            0xA0: 2, 0xA6: 2, 0xB6: 2, 0xAC: 3, 0xBC: 3,
            0xE6: 2, 0xF6: 2, 0xEE: 3, 0xFE: 3,
            0xC6: 2, 0xD6: 2, 0xCE: 3, 0xDE: 3,
            0xCA: 1, 0xE8: 1, 0x88: 1, 0xC8: 1,
            0x85: 2, 0x95: 2, 0x8D: 3, 0x9D: 3, 0x99: 3, 0x81: 2, 0x91: 2,
            0x86: 2, 0x96: 2, 0x8E: 3,
            0x84: 2, 0x94: 2, 0x8C: 3,
            0xEA: 1,
            0xAA: 1, 0x8A: 1, 0xA8: 1, 0x98: 1, 0x9A: 1, 0xBA: 1,
        }
        self.numops = { # This is the number of bytes that the operands evaluate to.
            0x69: 1, 0x65: 1, 0x75: 1, 0x6D: 1, 0x7D: 1, 0x79: 1, 0x61: 1, 0x71: 1,
            0x29: 1, 0x25: 1, 0x35: 1, 0x2D: 1, 0x3D: 1, 0x39: 1, 0x21: 1, 0x31: 1, 
            0x0A: 0, 0x06: 1, 0x16: 1, 0x0E: 1, 0x1E: 1,
            0x24: 1, 0x2C: 1,
            0xA9: 1, 0xA5: 1, 0xB5: 1, 0xAD: 1, 0xBD: 1, 0xB9: 1, 0xA1: 1, 0xB1: 1,
            0xA2: 1, 0xA6: 1, 0xB6: 1, 0xAE: 1, 0xBE: 1,
            0xA0: 1, 0xA6: 1, 0xB6: 1, 0xAC: 1, 0xBC: 1,
            0xE6: 1, 0xF6: 1, 0xEE: 2, 0xFE: 2,
            0xC6: 1, 0xD6: 1, 0xCE: 2, 0xDE: 2,
            0xCA: 0, 0xE8: 0, 0x88: 0, 0xC8: 0,
            0x85: 1, 0x95: 1, 0x8D: 2, 0x9D: 2, 0x99: 2, 0x81: 1, 0x91: 1,
            0x86: 1, 0x96: 1, 0x8E: 2,
            0x84: 1, 0x94: 1, 0x8C: 2,
            0xEA: 0,
            0xAA: 0, 0x8A: 0, 0xA8: 0, 0x98: 0, 0x9A: 0, 0xBA: 0,
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
    def impl(self, op1, op2, code):
        pass
    def flag(self, flag, bitval=None):
        if bitval is not None:
            self.stat |= self.statbits[flag.lower()]
    def adc_(self, op1, op2, code):
        c_in = 0 if (self.stat & self.statbits["c"]) else 1
        old_a = self.a
        
        op1_not = op1 & 0xFF
        result = old_a + op1_not + c_in
        
        self.a = result & 0xFF
        
        # Flags accept direct boolean expressions
        self.flag("c", result > 0xFF)
        self.flag("z", self.a == 0)
        self.flag("n", bool(self.a & 0x80))
        self.flag("v", bool((old_a ^ self.a) & (op1_not ^ self.a) & 0x80))
    def sbc_(self, op1, op2, code):
        c_in = 1 if (self.stat & self.statbits["c"]) else 0
        old_a = self.a
        
        op1_not = (~op1) & 0xFF
        result = old_a + op1_not + c_in
        
        self.a = result & 0xFF
        
        # Flags accept direct boolean expressions
        self.flag("c", result > 0xFF)
        self.flag("z", self.a == 0)
        self.flag("n", bool(self.a & 0x80))
        self.flag("v", bool((old_a ^ self.a) & (op1_not ^ self.a) & 0x80))

    def and_(self, op1):
        self.a &= op1
        if self.a == 0:
            self.flag("Z", bitval=True)
        else:
            self.flag("Z", bitval=False)
            
        if self.a & 0x80:
            self.flag("N", bitval=True)
        else:
            self.flag("N", bitval=False)
    def asl_(self, op1, op2, code):
        if code == 0x0A:
            self.a <<1
            self.a %= 0x100
        else:
            self.mem[op1 + 256*op2] <<= 1
            self.mem[op1 + 256*op2] %= 0x100
    def bit_(self, op1, op2, code):
        if self.a & (self.value + 256+self.val2) == 0x00:
            self.flag("Z", bitval=True)
        else:  
            self.flag("Z", bitval=False)
        if self.value & 0x80:
            self.flag("N", bitval=True)
        else:  
            self.flag("N", bitval=False)
        if self.value & 0x40:
            self.flag("V", bitval=True)
        else:  
            self.flag("V", bitval=False)
    def lda_(self, op1, op2, code):
        self.a = op1
        if self.a == 0:
            self.flag("Z", bitval=True)
        else:
            self.flag("Z", bitval=False)
            
        if self.a & 0x80:
            self.flag("N", bitval=True)
        else:
            self.flag("N", bitval=False)
    def ldx_(self, op1, op2, code):
        self.x = op1
        if self.x == 0:
            self.flag("Z", bitval=True)
        else:
            self.flag("Z", bitval=False)
            
        if self.x & 0x80:
            self.flag("N", bitval=True)
        else:
            self.flag("N", bitval=False)
    def ldy_(self, op1, op2, code):
        self.y = op1
        if self.y == 0:
            self.flag("Z", bitval=True)
        else:
            self.flag("Z", bitval=False)
            
        if self.y & 0x80:
            self.flag("N", bitval=True)
        else:
            self.flag("N", bitval=False)
    def sta_(self, op1, op2, code):
        self.mem[op1 + 256*op2] = self.a
    def stx_(self, op1, op2, code):
        self.mem[op1 + 256*op2] = self.x
    def sty_(self, op1, op2, code):
        self.mem[op1 + 256*op2] = self.y
    def dec_(self, op1, op2, code):
        self.mem[op1 + 256*op2] -= 1
    def inc_(self, op1, op2, code):
        self.mem[op1 + 256*op2] -= 1
    def dex_(self, op1, op2, code):
        self.x -= 1
    def dey_(self, op1, op2, code):
        self.y -= 1
    def inx_(self, op1, op2, code):
        self.x += 1
    def iny_(self, op1, op2, code):
        self.y += 1
    def jmp_(self, op1, op2, code):
        self.pc = op1 + 256*op2
    def nop_(self, op1, op2, code):
        pass
    def tax_(self, op1, op2, code):
        self.x = self.a
    def tay_(self, op1, op2, code):
        self.y = self.a
    def tsx_(self, op1, op2, code):
        self.x = self.sp
    def txa_(self, op1, op2, code):
        self.a = self.x
    def txs_(self, op1, op2, code):
        self.sp = self.x
    def tya_(self, op1, op2, code):
        self.a = self.y
    def executeinst(self):
        self.curr = self.mem[self.pc]
        self.next = self.mem[self.pc+1]
        self.next2 = self.mem[self.pc+2]
        self.addrmodes[self.curr](self.next, self.next2, self.curr)
        if self.numops[self.curr] == 2:
            self.mnem[self.curr](self.value, self.val2)
        elif self.numops[self.curr] == 1:
            self.val2 = 0
            self.mnem[self.curr](self.value)
        elif self.numops[self.curr] == 0:
            self.mnem[self.curr]()
class Attempt6502_Window:
    def __init__(self, width=800, height=600, title="Attempt-6502"):
        pygame.init()
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((0,128,0))
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
        sys.exit()
if __name__ == "__main__":
    cpu = CPU()
    disp = Attempt6502_Window()
    disp.run()
# Upcycle 3 Version
# Next Steps:
# CPU:
# ADC AND ASL BCC BCS BEQ BIT BMI BNE BPL BRK BVC BVS CLC
#  ✓   ✓   ✓   X   X   X   ✓   X   X   X   X   X   X  HI4
# CLD CLI CLV CMP CPX CPY DEC DEX DEY EOR INC INX INY JMP
# HI4 HI4 HI4 LO4 LO4 LO4  ✓   ✓   ✓   X   ✓   ✓   ✓   ✓  
# JSR LDA LDX LDY LSR NOP ORA PHA PHP PLA PLP ROL ROR RTI
#  X   ✓   ✓   ✓   X   ✓   X   X   X   X   X   X   X   X 
# RTS SBC SEC SED SEI STA STX STY TAX TAY TSX TXA TXS TYA
#  X   ✓  HI4 HI4 HI4  ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓ 
# PYGAME INITIALIZATION ✓
# REGISTER DISPLAY
# FLAGS
# MEMORY
# DISASSEMBLY
# CODE EDITOR
