import random
import vsc

from isa.info import (InstrGroupTy, InstrFormatTy, InstrNameTy, RegTy)

@vsc.randobj
class Instr:
    def __init__(self):
        self.XLEN = 32

        self.group = vsc.rand_enum_t(InstrGroupTy)
        self.format = vsc.rand_enum_t(InstrFormatTy)
        self.name = vsc.rand_enum_t(InstrNameTy)
        self.imm_len = vsc.bit_t(5)

        self.rs2 = vsc.rand_enum_t(RegTy)
        self.rs1 = vsc.rand_enum_t(RegTy)
        self.rd = vsc.rand_enum_t(RegTy)
        self.imm = vsc.rand_bit_t(2**self.imm_len)

    def get_name(self) -> str:
        return self.name.name

    def get_imm(self):
        return self.imm

    def into_asm(self) -> str:
        if self.format == InstrFormatTy.InstFormatJ:
            return f'{self.name.name} {self.rd.name}, {self.get_imm()}'
        elif self.format == InstrFormatTy.InstFormatR:
            return f'{self.name.name} {self.rd.name}, {self.rs1.name}, {self.rs2.name}'
        else:
            assert(0)

def generate() -> Instr:
    ret = Instr()
    vsc.randomize(ret)
    return ret
