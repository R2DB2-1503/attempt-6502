import pygame, sys
class CPU:
    def __init__(self):
        self.mem = [0x00] * 65536
        self.a = 0x00
        self.x = 0x00
        self.y = 0x00
        self.pc = 0x8000
        self.irq = 0x8000
        self.rst = 0x8000
        self.nmi = 0x8000
        self.sp = 0xFF
        self.stat = 0b00100000
        self.curr = self.mem[self.pc]
        self.next = self.mem[self.pc+1]
        self.next2 = self.mem[self.pc+2]
        self.ver = "α1u"
        self.value = 0x00
        self.val2 = 0x00
        self.mnem = {
            0x69: self.adc_, 0x65: self.adc_, 0x75: self.adc_, 0x6D: self.adc_, 0x7D: self.adc_, 0x79: self.adc_, 0x61: self.adc_, 0x71: self.adc_,
            0x29: self.and_, 0x25: self.and_, 0x35: self.and_, 0x2D: self.and_, 0x3D: self.and_, 0x39: self.and_, 0x21: self.and_, 0x31: self.and_,
            0x0A: self.asl_, 0x06: self.asl_, 0x16: self.asl_, 0x0E: self.asl_, 0x1E: self.asl_,
            0x4A: self.lsr_, 0x46: self.lsr_, 0x56: self.lsr_, 0x4E: self.lsr_, 0x5E: self.lsr_,
            0x2A: self.rol_, 0x26: self.rol_, 0x36: self.rol_, 0x2E: self.rol_, 0x3E: self.rol_,
            0x6A: self.ror_, 0x66: self.ror_, 0x76: self.ror_, 0x6E: self.ror_, 0x7E: self.ror_,
            0x24: self.bit_, 0x2C: self.bit_,
            0xA9: self.lda_, 0xA5: self.lda_, 0xB5: self.lda_, 0xAD: self.lda_, 0xBD: self.lda_, 0xB9: self.lda_, 0xA1: self.lda_, 0xB1: self.lda_,
            0xA2: self.ldx_, 0xA6: self.ldx_, 0xB6: self.ldx_, 0xAE: self.ldx_, 0xBE: self.ldx_,
            0xA0: self.ldy_, 0xA4: self.ldy_, 0xB6: self.ldy_, 0xAC: self.ldy_, 0xBC: self.ldy_,
            0xE6: self.inc_, 0xF6: self.inc_, 0xEE: self.inc_ , 0xFE: self.inc_,
            0xC6: self.dec_, 0xD6: self.dec_, 0xCE: self.dec_, 0xDE: self.dec_,
            0xCA: self.dex_, 0xE8: self.inx_, 0x88: self.dey_, 0xC8: self.iny_,
            0x85: self.sta_, 0x95: self.sta_, 0x8D: self.sta_, 0x9D: self.sta_, 0x99: self.sta_, 0x81: self.sta_, 0x91: self.sta_,
            0x86: self.stx_, 0x96: self.stx_, 0x8E: self.stx_,
            0x84: self.sty_, 0x94: self.sty_, 0x8C: self.sty_,
            0xEA: self.nop_, 0xAA: self.tax_, 0x8A: self.txa_, 0xA8: self.tay_, 0x98: self.tya_, 0x9A: self.txs_, 0xBA: self.tsx_,
            0xC9: self.cmp_, 0xC5: self.cmp_, 0xD5: self.cmp_, 0xCD: self.cmp_, 0xDD: self.cmp_, 0xD9: self.cmp_, 0xC1: self.cmp_, 0xD1: self.cmp_,
            0xE0: self.cpx_, 0xE4: self.cpx_, 0xEC: self.cpx_,
            0xC0: self.cpy_, 0xC4: self.cpy_, 0xCC: self.cpy_,
            0x00: self.brk_,
            0x18: self.clc_, 0x38: self.sec_, 0x58: self.cli_, 0x78: self.sei_, 0xB8: self.clv_, 0xD8: self.cld_, 0xF8: self.sed_,
            0x09: self.ora_, 0x05: self.ora_, 0x15: self.ora_, 0x0D: self.ora_, 0x1D: self.ora_, 0x19: self.ora_, 0x01: self.ora_, 0x11: self.ora_,
            0x49: self.eor_, 0x45: self.eor_, 0x55: self.eor_, 0x4D: self.eor_, 0x5D: self.eor_, 0x59: self.eor_, 0x41: self.eor_, 0x51: self.eor_,
            0x48: self.pha_, 0x68: self.pla_, 0x08: self.php_, 0x28: self.plp_,
            0x10: self.bpl_, 0x30: self.bmi_, 0x50: self.bvc_, 0x70: self.bvs_, 0x90: self.bcc_, 0xB0: self.bcs_, 0xD0: self.bne_, 0xF0: self.beq_,
            0x20: self.jsr_,
            0x60: self.rts_,
            0x40: self.rti_,
        }
        self.statbits = {
            "n": 0x80, "v": 0x40, "-": 0x20, "b": 0x10,
            "d": 0x08, "i": 0x04, "z": 0x02, "c": 0x01,
        }
        self.addrmodes = {
            0x69: self.imd, 0x65: self.zp, 0x75: self.zpix, 0x6D: self.abslt, 0x7D: self.absix, 0x79: self.absiy, 0x61: self.indix, 0x71: self.indiy,
            0x29: self.imd, 0x25: self.zp, 0x35: self.zpix, 0x2D: self.abslt, 0x3D: self.absix, 0x39: self.absiy, 0x21: self.indix, 0x31: self.indiy,
            0x0A: self.acc, 0x06: self.zp, 0x16: self.zpix_, 0x0E: self.abslt_, 0x1E: self.absix_,
            0x4A: self.acc, 0x46: self.zp, 0x56: self.zpix_, 0x4E: self.abslt_, 0x5E: self.absix_,
            0x2A: self.acc, 0x26: self.zp, 0x36: self.zpix_, 0x2E: self.abslt_, 0x5E: self.absix_,
            0x6A: self.acc, 0x66: self.zp, 0x76: self.zpix_, 0x6E: self.abslt_, 0x7E: self.absix_,
            0x24: self.zp, 0x2C: self.abslt,
            0xA9: self.imd, 0xA5: self.zp, 0xB5: self.zpix, 0xAD: self.abslt, 0xBD: self.absix, 0xB9: self.absiy, 0xA1: self.indix, 0xB1: self.indiy,
            0xA2: self.imd, 0xA6: self.zp, 0xB6: self.zpix, 0xAE: self.abslt, 0xBE: self.absix,
            0xA0: self.imd, 0xA6: self.zp, 0xB6: self.zpix, 0xAC: self.abslt, 0xBC: self.absix,
            0xE6: self.zp, 0xF6: self.zpix, 0xEE: self.abslt, 0xFE: self.absix,
            0xC6: self.zp, 0xD6: self.zpix, 0xCE: self.abslt, 0xDE: self.absix,
            0xCA: self.impl, 0xE8: self.impl, 0x88: self.impl, 0xC8: self.impl,
            0x85: self.zp_, 0x95: self.zpix_, 0x8D: self.abslt_, 0x9D: self.absix_, 0x99: self.absiy_, 0x81: self.indix, 0x91: self.indiy,
            0x86: self.zp_, 0x96: self.zpiy_, 0x8E: self.abslt_,
            0x84: self.zp_, 0x94: self.zpix_, 0x8C: self.abslt_,
            0xEA: self.impl, 0xAA: self.impl, 0x8A: self.impl, 0xA8: self.impl, 0x98: self.impl, 0x9A: self.impl, 0xBA: self.impl,
            0xC9: self.imd, 0xC5: self.zp, 0xD5: self.zpix, 0xCD: self.abslt, 0xDD: self.absix, 0xD9: self.absiy, 0xC1: self.indix, 0xD1: self.indiy,
            0xE0: self.imd, 0xE4: self.zp, 0xEC: self.abslt,
            0xC0: self.imd, 0xC4: self.zp, 0xCC: self.abslt,
            0x00: self.impl,
            0x18: self.impl, 0x38: self.impl, 0x58: self.impl, 0x78: self.impl, 0xB8: self.impl, 0xD8: self.impl, 0xF8: self.impl,
            0x09: self.imd, 0x05: self.zp, 0x15: self.zpix, 0x0D: self.abslt, 0x1D: self.absix, 0x19: self.absiy, 0x01: self.indix, 0x11: self.indiy,       
            0x49: self.imd, 0x45: self.zp, 0x55: self.zpix, 0x4D: self.abslt, 0x5D: self.absix, 0x59: self.absiy, 0x41: self.indix, 0x51: self.indiy,
            0x48: self.impl, 0x68: self.impl, 0x08: self.impl, 0x28: self.impl,
            0x10: self.rel, 0x30: self.rel, 0x50: self.rel, 0x70: self.rel, 0x90: self.rel, 0xB0: self.rel, 0xD0: self.rel, 0xF0: self.rel,
            0x20: self.abslt,
            0x60: self.impl,
            0x40: self.impl,
        }
        self.numbytes = {
            0x69: 2, 0x65: 2, 0x75: 2, 0x6D: 3, 0x7D: 3, 0x79: 3, 0x61: 2, 0x71: 2,
            0x29: 2, 0x25: 2, 0x35: 2, 0x2D: 3, 0x3D: 3, 0x39: 3, 0x21: 2, 0x31: 2, 
            0x0A: 1, 0x06: 2, 0x16: 2, 0x0E: 3, 0x1E: 3,  
            0x4A: 1, 0x46: 2, 0x56: 2, 0x4E: 3, 0x5E: 3,
            0x2A: 1, 0x26: 2, 0x36: 2, 0x2E: 3, 0x3E: 3,  
            0x6A: 1, 0x66: 2, 0x76: 2, 0x6E: 3, 0x7E: 3,                            
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
            0xC9: 2, 0xC5: 2, 0xD5: 2, 0xCD: 3, 0xDD: 3, 0xD9: 3, 0xC1: 2, 0xD1: 2,
            0xE0: 2, 0xE4: 2, 0xEC: 3,
            0xC0: 2, 0xC4: 2, 0xCC: 3,
            0x00: 1,
            0x18: 1, 0x38: 1, 0x58: 1, 0x78: 1, 0xB8: 1, 0xD8: 1, 0xF8: 1,
            0x09: 2, 0x05: 2, 0x15: 2, 0x0D: 3, 0x1D: 3, 0x19: 3, 0x01: 2, 0x11: 2,
            0x49: 2, 0x45: 2, 0x55: 2, 0x4D: 3, 0x5D: 3, 0x59: 3, 0x41: 2, 0x51: 2,
            0x48: 1, 0x68: 1, 0x08: 1, 0x28: 1,
            0x10: 2, 0x30: 2, 0x50: 2, 0x70: 2, 0x90: 2, 0xB0: 2, 0xD0: 2, 0xF0: 2,
            0x20: 3,
            0x60: 1,
            0x40: 1,
        }
        self.numops = { # This is number of bytes that operands evaluate to.
            0x69: 1, 0x65: 1, 0x75: 1, 0x6D: 1, 0x7D: 1, 0x79: 1, 0x61: 1, 0x71: 1,
            0x29: 1, 0x25: 1, 0x35: 1, 0x2D: 1, 0x3D: 1, 0x39: 1, 0x21: 1, 0x31: 1, 
            0x0A: 0, 0x06: 1, 0x16: 1, 0x0E: 1, 0x1E: 1,
            0x4A: 0, 0x46: 1, 0x56: 1, 0x4E: 1, 0x5E: 1,
            0x2A: 0, 0x26: 1, 0x36: 1, 0x2E: 1, 0x3E: 1,
            0x6A: 0, 0x66: 1, 0x76: 1, 0x6E: 1, 0x7E: 1,
            0x24: 1, 0x2C: 1,
            0xA9: 1, 0xA5: 1, 0xB5: 1, 0xAD: 1, 0xBD: 1, 0xB9: 1, 0xA1: 1, 0xB1: 1,
            0xA2: 1, 0xA6: 1, 0xB6: 1, 0xAE: 1, 0xBE: 1,
            0xA0: 1, 0xA6: 1, 0xB6: 1, 0xAC: 1, 0xBC: 1,
            0xE6: 1, 0xF6: 1, 0xEE: 2, 0xFE: 2,
            0xC6: 1, 0xD6: 1, 0xCE: 2, 0xDE: 2,
            0xCA: 0, 0xE8: 0, 0x88: 0, 0xC8: 0,
            0x85: 1, 0x95: 1, 0x8D: 1, 0x9D: 1, 0x99: 1, 0x81: 1, 0x91: 1,
            0x86: 1, 0x96: 1, 0x8E: 1,
            0x84: 1, 0x94: 1, 0x8C: 1,
            0xEA: 0,
            0xAA: 0, 0x8A: 0, 0xA8: 0, 0x98: 0, 0x9A: 0, 0xBA: 0,
            0xC9: 1, 0xC5: 1, 0xD5: 1, 0xCD: 1, 0xDD: 1, 0xD9: 1, 0xC1: 1, 0xD1: 1,
            0xE0: 1, 0xE4: 1, 0xEC: 1,
            0xC0: 1, 0xC4: 1, 0xCC: 1,
            0x00: 0,
            0x18: 1, 0x38: 1, 0x58: 1, 0x78: 1, 0xB8: 1, 0xD8: 1, 0xF8: 1,
            0x09: 1, 0x05: 1, 0x15: 1, 0x0D: 1, 0x1D: 1, 0x19: 1, 0x01: 1, 0x11: 1,
            0x49: 1, 0x45: 1, 0x55: 1, 0x4D: 1, 0x5D: 1, 0x59: 1, 0x41: 1, 0x51: 1,
            0x48: 0, 0x68: 0, 0x08: 0, 0x28: 0,
            0x10: 2, 0x30: 2, 0x50: 2, 0x70: 2, 0x90: 2, 0xB0: 2, 0xD0: 2, 0xF0: 2,
            0x20: 2,
            0x60: 0,
            0x40: 0,
        }
        self.addrsym = { # In form Mode, Prefix, Suffix
            self.imd: ["#$",""],
            self.zp: ["$",""],
            self.zp_: ["$",""],
            self.zpix_: ["$",",X"],
            self.zpix: ["$",",X"],
            self.zpiy_: ["$",",Y"],
            self.zpiy: ["$",",Y"],
            self.abslt: ["$",""],
            self.abslt_: ["$",""],
            self.acc: ["A",""],
            self.rel: ["R",""],
            self.absix: ["$",",X"],
            self.absix_: ["$",",X"],
            self.absiy: ["$",",Y"],
            self.absiy_: ["$",",Y"],
            self.indir: ["[$","]"],
            self.indix: ["[$",",X]"],
            self.indiy: ["[$","],Y"],
        }
    def imd(self, op1, op2, code):
        self.value = op1
    def zp(self, op1, op2, code):
        self.value = self.mem[op1]
    def zp_(self, op1, op2, code):
        self.value = op1
    def zpix_(self, op1, op2, code):
        self.value = op1
    def zpix(self, op1, op2, code):
        self.value = self.mem[(op1 + self.x) % 0x100]
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
            if bitval:
                self.stat |= self.statbits[flag.lower()]
            else:
                self.stat &= ~(self.statbits[flag.lower()])
    def adc_(self, op1=None, op2=None, code=None):
        c_in = 0 if (self.stat & self.statbits["c"]) else 256
        old_a = self.a
        op1_not = op1 & 0xFF
        result = old_a + op1_not + c_in
        self.a = result & 0xFF
        self.flag("c", result > 0xFF)
        self.flag("z", self.a == 0)
        self.flag("n", bool(self.a & 0x80))
        self.flag("v", bool((old_a ^ self.a) & (op1_not ^ self.a) & 0x80))
    def sbc_(self, op1=None, op2=None, code=None):
        c_in = 1 if (self.stat & self.statbits["c"]) else 0
        old_a = self.a
        op1_not = (~op1) & 0xFF
        result = old_a + op1_not + c_in
        self.a = result & 0xFF
        self.flag("c", result > 0xFF)
        self.flag("z", self.a == 0)
        self.flag("n", bool(self.a & 0x80))
        self.flag("v", bool((old_a ^ self.a) & (op1_not ^ self.a) & 0x80))
    def and_(self, op1=None, op2=None, code=None):
        self.a &= op1
        if self.a == 0:
            self.flag("Z", bitval=True)
        else:
            self.flag("Z", bitval=False)
        if self.a & 0x80:
            self.flag("N", bitval=True)
        else:
            self.flag("N", bitval=False)
    def asl_(self, op1=None, op2=None, code=None):
        is_accumulator = (code == 0x0A)
        addr = op1 + 256 * op2 if not is_accumulator else None
        val = self.a if is_accumulator else self.mem[addr]
        if val & 0x80:
            self.sec_()
        else:
            self.clc_()
        val = (val << 1) & 0xFF
        self.flag("N", bitval=bool(val & 0x80))
        self.flag("Z", bitval=bool(val == 0x00))
        if is_accumulator:
            self.a = val
        else:
            self.mem[addr] = val
    def lsr_(self, op1=None, op2=None, code=None):
        is_accumulator = (code == 0x4A)
        addr = op1 + 256 * op2 if not is_accumulator else None
        val = self.a if is_accumulator else self.mem[addr]
        if val & 0x01:
            self.sec_()
        else:
            self.clc_() 
        val >>= 1
        self.flag("N", bitval=False)
        self.flag("Z", bitval=bool(val == 0x00))
        if is_accumulator:
            self.a = val
        else:
            self.mem[addr] = val
    def rol_(self, op1=None, op2=None, code=None):
        is_accumulator = (code == 0x2A)
        addr = op1 + 256 * op2 if not is_accumulator else None
        val = self.a if is_accumulator else self.mem[addr]
        old_carry = 1 if self.get_carry() else 0 
        if val & 0x80:
            self.sec_()
        else:
            self.clc_()
        val = ((val << 1) | old_carry) & 0xFF
        self.flag("N", bitval=bool(val & 0x80))
        self.flag("Z", bitval=bool(val == 0x00))
        if is_accumulator:
            self.a = val
        else:
            self.mem[addr] = val
    def ror_(self, op1=None, op2=None, code=None):
        is_accumulator = (code == 0x6A)
        addr = op1 + 256 * op2 if not is_accumulator else None
        val = self.a if is_accumulator else self.mem[addr]
        old_carry = 0x80 if self.get_carry() else 0 
        if val & 0x01:
            self.sec_()
        else:
            self.clc_()
        val = (val >> 1) | old_carry
        self.flag("N", bitval=bool(val & 0x80))
        self.flag("Z", bitval=bool(val == 0x00))
        if is_accumulator:
            self.a = val
        else:
            self.mem[addr] = val
    def bit_(self, op1=None, op2=None, code=None):
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
    def lda_(self, op1=None, op2=None, code=None):
        self.a = op1
        if self.a == 0:
            self.flag("Z", bitval=True)
        else:
            self.flag("Z", bitval=False)
        if self.a & 0x80:
            self.flag("N", bitval=True)
        else:
            self.flag("N", bitval=False)
    def ldx_(self, op1=None, op2=None, code=None):
        self.x = op1
        if self.x == 0:
            self.flag("Z", bitval=True)
        else:
            self.flag("Z", bitval=False)
        if self.x & 0x80:
            self.flag("N", bitval=True)
        else:
            self.flag("N", bitval=False)
    def ldy_(self, op1=None, op2=None, code=None):
        self.y = op1
        if self.y == 0:
            self.flag("Z", bitval=True)
        else:
            self.flag("Z", bitval=False)            
        if self.y & 0x80:
            self.flag("N", bitval=True)
        else:
            self.flag("N", bitval=False)
    def sta_(self, op1=None, op2=None, code=None):
        self.mem[op1 + 256*op2] = self.a
    def stx_(self, op1=None, op2=None, code=None):
        self.mem[op1 + 256*op2] = self.x
    def sty_(self, op1=None, op2=None, code=None):
        self.mem[op1 + 256*op2] = self.y
    def dec_(self, op1=None, op2=None, code=None):
        self.mem[op1 + 256*op2] -= 1
    def inc_(self, op1=None, op2=None, code=None):
        self.mem[op1 + 256*op2] -= 1
    def dex_(self, op1=None, op2=None, code=None):
        self.x -= 1
    def dey_(self, op1=None, op2=None, code=None):
        self.y -= 1
    def inx_(self, op1=None, op2=None, code=None):
        self.x += 1
    def iny_(self, op1=None, op2=None, code=None):
        self.y += 1
    def jmp_(self, op1=None, op2=None, code=None):
        self.pc = op1 + 256*op2
    def nop_(self, op1=None, op2=None, code=None):
        pass
    def tax_(self, op1=None, op2=None, code=None):
        self.x = self.a
    def tay_(self, op1=None, op2=None, code=None):
        self.y = self.a
    def tsx_(self, op1=None, op2=None, code=None):
        self.x = self.sp
    def txa_(self, op1=None, op2=None, code=None):
        self.a = self.x
    def txs_(self, op1=None, op2=None, code=None):
        self.sp = self.x
    def tya_(self, op1=None, op2=None, code=None):
        self.a = self.y
    def cmp_(self, op1=None, op2=None, code=None):
        self.flag("Z", bitval=bool(self.a == op1))
        self.flag("N", bitval=bool(self.a < op1))
        self.flag("C", bitval=bool(self.a >= op1))
    def cpx_(self, op1=None, op2=None, code=None):
        self.flag("Z", bitval=bool(self.x == op1))
        self.flag("N", bitval=bool(self.x < op1))
        self.flag("C", bitval=bool(self.x >= op1))
    def cpy_(self, op1=None, op2=None, code=None):
        self.flag("Z", bitval=bool(self.y == op1))
        self.flag("N", bitval=bool(self.y < op1))
        self.flag("C", bitval=bool(self.y >= op1))
    def brk_(self, op1=None, op2=None, code=None):
        if self.stat & self.statbits["B".lower()] and self.pc != 0x8000:
            self.flag("B", bitval=True)
            self.pc -= 1
            print("HALT: BRK Reached.")
    def clc_(self, op1=None, op2=None, code=None):
        self.flag("C", bitval=False)
    def sec_(self, op1=None, op2=None, code=None):
        self.flag("C", bitval=True)
    def cld_(self, op1=None, op2=None, code=None):
        self.flag("D", bitval=False)
    def sed_(self, op1=None, op2=None, code=None):
        self.flag("D", bitval=True)
    def clv_(self, op1=None, op2=None, code=None):
        self.flag("V", bitval=False)
    def cli_(self, op1=None, op2=None, code=None):
        self.flag("I", bitval=False)
    def sei_(self, op1=None, op2=None, code=None):
        self.flag("I", bitval=True)
    def ora_(self, op1=None, op2=None, code=None):
        self.a |= op1
    def eor_(self, op1=None, op2=None, code=None):
        self.a ^= op1
    def pha_(self, op1=None, op2=None, code=None):
        self.sp -= 1
        self.mem[self.sp + 0x100] = self.a
    def php_(self, op1=None, op2=None, code=None):
        self.sp -= 1
        self.sp &= 0xFF
        self.mem[self.sp + 0x100] = self.stat
    def pla_(self, op1=None, op2=None, code=None):
        self.stat = self.mem[self.sp + 0x100]
        self.sp += 1
        self.sp &= 0xFF
    def plp_(self, op1=None, op2=None, code=None):
        self.stat = self.mem[self.sp + 0x100]
        self.sp += 1
        self.sp &= 0xFF
    def bpl_(self, op1=None, op2=None, code=None):
        if not self.stat & 0x80:
            self.jmp_(op1, op2)
    def bmi_(self, op1=None, op2=None, code=None):
        if self.stat & 0x80:
            self.jmp_(op1, op2)
    def bvc_(self, op1=None, op2=None, code=None):
        if not self.stat & 0x40:
            self.jmp_(op1, op2)
    def bvs_(self, op1=None, op2=None, code=None):
        if self.stat & 0x40:
            self.jmp_(op1, op2)
    def bcc_(self, op1=None, op2=None, code=None):
        if not self.stat & 0x01:
            self.jmp_(op1, op2)
    def bcs_(self, op1=None, op2=None, code=None):
        if self.stat & 0x01:
            self.jmp_(op1, op2)
    def bne_(self, op1=None, op2=None, code=None):
        if not self.stat & 0x02:
            self.jmp_(op1, op2)
    def beq_(self, op1=None, op2=None, code=None):
        if self.stat & 0x02:
            self.jmp_(op1, op2)
    def jsr_(self, op1=None, op2=None, code=None):
        targ = (op2 << 8) | op1
        ret = self.pc - 1
        self.mem[0x0100 + self.s] = (ret >> 8) & 0xFF
        self.sp = (self.sp - 1) & 0xFF
        self.mem[0x0100 + self.s] = ret & 0xFF
        self.sp = (self.s - 1) & 0xFF
        self.pc = targ
    def rts_(self, op1=None, op2=None, code=None):
        self.sp = (self.sp) +1
        jl = self.mem[0x100 + self.sp]
        self.s = (self.s + 1) & 0xFF
        jh = self.mem[0x0100 + self.sp]
        fja = ((jh << 8) | jl) + 1
        self.pc = fja
    def rti_(self, op1=None, op2=None, code=None):
        self.plp_()
        tempa = self.a
        self.pla_()
        high = self.a
        self.pla_()
        low = self.a
        self.a = tempa
        self.jmp(low, high)
    def irq_(self, op1=None, op2=None, code=None):
        if self.stat & 0x04:
            pass
        else:
            self.interrupt_seq_(self.irq)
    def nmi_(self, op1=None, op2=None, code=None):
        self.interrupt_seq_(self.nmi)
    def interrupt_seq_(self, addr):
        high = (self.pc & 0xFF00) >> 8
        low = (self.pc & 0x00FF)
        tempa = self.a
        self.a = high
        self.pha_()
        self.a = low
        self.pha_()
        self.php_()
        self.a = tempa
        ihigh = (addr & 0xFF00) >> 8
        ilow = (addr & 0x00FF)
        self.jmp_(ilow, ihigh)
    def executeinst(self):
        self.curr = self.mem[self.pc]
        self.next = self.mem[self.pc+1]
        self.next2 = self.mem[self.pc+2]
        self.addrmodes[self.curr](self.next, self.next2, self.curr)
        self.mnem[self.curr](self.value, self.val2, self.curr)
        self.pc += self.numbytes[self.curr]
    def reset_(self):
        self.a = 0x00
        self.x = 0x00
        self.y = 0x00
        self.nmi = self.mem[0xfffa] + 256*self.mem[0xfffb]
        self.pc = self.mem[0xfffc] + 256*self.mem[0xfffd]
        self.irq = self.mem[0xfffe] + 256*self.mem[0xffff]
        self.sp = 0xFF
        self.stat = 0b00100000
        self.curr = self.mem[self.pc]
        self.next = self.mem[self.pc+1]
        self.next2 = self.mem[self.pc+2]
        self.value = 0x00
        self.val2 = 0x00
class Attempt6502_Window:
    def __init__(self, width=1800, height=700, title="Attempt-6502"):
        pygame.init()
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.font = pygame.font.SysFont("Cascadia Code", 24)
        self.page = 0x00
        self.darkascii = 0
    def render_text(self, text, x, y, color=0x000000, antialias=True):
        red = (color & 0xFF0000) >> 16
        green = (color & 0x00FF00) >> 8
        blue = (color & 0x0000FF) >> 0
        surface = self.font.render(text, antialias, (red, green, blue))
        self.screen.blit(surface, (x,y))
    def regdisplay(self, a, x, y, pc, sr, sp):
        self.render_text(f"a=${a:02x}", 20, 20, 0xFF0000)
        self.render_text(f"x=${x:02x}", 20, 60, 0x00FF00)
        self.render_text(f"y=${y:02x}", 20, 100, 0x0000FF)
        self.render_text(f"pc=${pc:04x}", 20, 140, 0x00FFFF)
        self.render_text(f"${pc:04x}", 300, 20, 0x00FFFF)
        self.render_text(f"sp=${sp:02x}", 20, 180, 0xFF00FF)
        self.render_text(f"sr=%{sr:08b}", 20, 220, 0xFFFF00)
        self.render_text(f"   %nv-bdizc", 20, 260, 0xFFFF7F)
    def func_name(self, func):
        if isinstance(func, str):
            return func
        if func is None:
            return "UNK"
        if hasattr(func, '__name__'):
            return func.__name__
        return str(func)
    def char_(self, l):
        if l < 0x20:
            self.darkascii = 0x7F7F7F
            return "."
        self.darkascii = 0xFFFFFF
        return chr(l)
    def run(self):
        clock = pygame.time.Clock()
        running = True
        cpu.pc = cpu.mem[0xfffc] + 256*cpu.mem[0xfffd]
        while running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                cpu.executeinst()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        cpu.executeinst()
                    if event.key == pygame.K_UP:
                        self.page = (self.page + 0x10) & 0xFF
                    if event.key == pygame.K_DOWN:
                        self.page = (self.page - 0x10) & 0xFF
                    if event.key == pygame.K_LEFT:
                        self.page = (self.page - 0x01) & 0xFF
                    if event.key == pygame.K_RIGHT:
                        self.page = (self.page + 0x01) & 0xFF
                    if event.key == pygame.K_i:
                        if event.mod & pygame.KMOD_SHIFT:
                            cpu.nmi_()
                        else:
                            cpu.irq_()
                    if event.key == pygame.K_r:
                        if event.mod & pygame.KMOD_SHIFT:
                            cpu.reset_()
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.QUIT()
            self.screen.fill((0,0,0))
            self.regdisplay(cpu.a, cpu.x, cpu.y, cpu.pc, cpu.stat, cpu.sp)
            cpu.curr = cpu.mem[cpu.pc]
            cpu.next = cpu.mem[cpu.pc+1]
            cpu.next2 = cpu.mem[cpu.pc+2]
            butes = cpu.numbytes[cpu.curr]
            bwtes = cpu.numbytes[cpu.mem[cpu.pc + butes]]
            current_instr = cpu.mnem[cpu.curr]
            mnemonic = self.func_name(current_instr).rstrip('_').upper()
            mode_method = cpu.addrmodes[cpu.curr]
            symbols = cpu.addrsym.get(mode_method, ["", ""])
            prefix = symbols[0]
            suffix = symbols[1]
            if butes == 1:
                display_text = f"{mnemonic}"
            if butes == 2:
                display_text = f"{mnemonic} {prefix}{cpu.next:02x}{suffix}"
            if butes == 3:
                display_text = f"{mnemonic} {prefix}{cpu.next:02x}{cpu.next2:02x}{suffix}"
            pcdisasm = cpu.pc + butes
            self.render_text(display_text, 400, 20, 0xff7f00)
            for i in range(1,10+1,1):
                next_instr = cpu.mnem[cpu.mem[pcdisasm]]
                mnemonicnext = self.func_name(next_instr).rstrip('_').upper()
                mode_methodn = cpu.addrmodes[cpu.mem[pcdisasm]]
                symbolsn = cpu.addrsym.get(mode_methodn, ["", ""])
                prefixn = symbolsn[0]
                suffixn = symbolsn[1]
                if bwtes == 1:
                    display_text2 = f"{mnemonicnext}"
                if bwtes == 2:
                    display_text2 = f"{mnemonicnext} {prefixn}{cpu.mem[pcdisasm + 1]:02x}{suffix}"
                if bwtes == 3:
                    display_text2 = f"{mnemonic} {prefixn}{cpu.mem[pcdisasm + 1]:02x}{cpu.mem[pcdisasm + 2]:02x}{suffixn}"
                self.render_text(display_text2, 400, 20 + 40*i, 0xcc5c00)
                self.render_text(f"${pcdisasm:04x}", 300, 20 + 40*i, 0xcc5c00)
                pcdisasm += bwtes
                bwtes = cpu.numbytes[cpu.mem[pcdisasm]]
            self.render_text(f"{self.page:02x}", -1.25*45 + 650, 0*30 + 20, 0xFFFFFF)
            for j in range(16):
                self.render_text(f"0{j:01x}", j*45 + 650 , 0*30 + 20, 0xFFFFFF)
                self.render_text(f"{j:01x}", j*15 + 1500 , 0*30 + 20, 0xFFFFFF)
            for i in range(16):
                self.render_text(f"{i:01x}0", -1.25*45 + 650 , i*30 + 60, 0xFFFFFF)
                self.render_text(f"{i:01x}0", -1.25*45 + 1500 , i*30 + 60, 0xFFFFFF)
            for i in range(16):
                for j in range(16):
                    self.render_text(f"{cpu.mem[16*i + j + (self.page * 0x100)]:02x}", j*45 + 650 , i*30 + 60, 0xFFFFFF)
                    self.render_text(f"{self.char_(cpu.mem[16*i + j + (self.page * 0x100)])}", j*15 + 1500 , i*30 + 60, self.darkascii)
            self.render_text(cpu.ver, 20, 660, 0x444444)
            i = 330
            Controls = [
                "Controls:",
                "Space (Hold): Run",
                "N: Step",
                "I: IRQ",
                "Shift+R: Reset",
                "Shift+I: NMI",
            ]
            for item in Controls:
                self.render_text(item, 20, i, 0x7f7f7f)
                i += 30
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
        sys.exit()
if __name__ == "__main__":
    cpu = CPU()
    if len(sys.argv) > 1:
        bin_file_path = sys.argv[1]
        with open(bin_file_path, "rb") as file:
            raw_data = file.read()
            program = list(raw_data)
    else:
        while True:
            data = input("Enter bytes: ")
            start = input("Enter start point: ")
            print(data)
            program = [int(b, 16) for b in data.split()]
            for i in range(len(program)):
                cpu.mem[i+int(start,16)] = program[i]
            if start.lower() == "fffa":
                break
    disp = Attempt6502_Window()
    disp.run()
# Version: Alpha Upcycle 1
# Ready to Commit: YES
# To Do:
"""
"""
#                HIGH
# DOWN       UP
#      LOW
# Next Steps:
# CPU:
# ADC AND ASL BCC BCS BEQ BIT BMI BNE BPL BRK BVC BVS CLC
#  ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓ 
# CLD CLI CLV CMP CPX CPY DEC DEX DEY EOR INC INX INY JMP
#  ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓  
# JSR LDA LDX LDY LSR NOP ORA PHA PHP PLA PLP ROL ROR RTI
#  ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓ 
# RTS SBC SEC SED SEI STA STX STY TAX TAY TSX TXA TXS TYA
#  ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓ 
# RESET  ✓ 
# PYGAME INITIALIZATION ✓ 
# REGISTER DISPLAY ✓ 
# FLAGS ✓ 
# CURRENT INSTRUCTION ✓ 
# MEMORY VIEWER ✓ 
# PRIMITIVE CODE EDITOR ✓ 
# DISASSEMBLY ✓ 
# EXPAND MEMORY VIEWER TO DISPLAY ASCII ✓ 
# EXPAND DISASSEMBLY ✓ 
# CODE EDITOR on hiatus
# 128x64 SCREEN h07 start
