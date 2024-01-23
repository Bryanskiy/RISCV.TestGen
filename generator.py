import isa.instruction as instr
from enum import Enum
from typing import Any
import random
import textwrap
from dataclasses import dataclass
from typing import Sequence, ClassVar

import isa.info

from itertools import repeat
from isa.info import InstrFormatTy, InstrCategoryTy, InstrNameTy
from isa.info import IMM_DICT


ASM_PREAMBULE = textwrap.dedent(
    """
    .section .text

    .globl start

    start:
    """
)


@dataclass
class Generator:
    seed: int = 0
    adr_range: ClassVar[tuple[int, int]] = (0x10, 0x4000)

    def generateInstrNamed(self, name: isa.info.InstrNameTy) -> instr.Instruction:
        return instr.Instruction(
            name,
            self.__regGen(),
            self.__regGen(),
            self.__regGen(),
            self.__regGen(),
            self.__randgen(1 << isa.info.XLEN),
        )

    @staticmethod
    def __randgen(bound: int):
        return random.randint(0, bound - 1)

    @staticmethod
    def __regGen():
        return Generator.__randgen(1 << 5)

    def generateInstr(self, allowed: Sequence[isa.info.InstrNameTy]):
        name = random.choice(allowed)

        return self.generateInstrNamed(name)

    def generateMem(self, count: int = 10):
        addr_regval = random.randint(self.adr_range[0], self.adr_range[1])
        addr_offset = random.randint(
            0,
            min(
                max(abs(self.adr_range[i] - addr_regval) for i in range(2)),
                (1 << 12) - 1,
            ),
        )

        base = self.__regGen()

        def gen_preambula():
            return [
                instr.Instruction(isa.info.InstrNameTy.LUI, rd=base, imm=addr_regval),
                instr.Instruction(
                    isa.info.InstrNameTy.ADDI, rd=base, imm=addr_regval, rs1=0
                ),
            ]

        instr_stream = (
            gen_preambula()
            + [
                instr.Instruction(
                    isa.info.InstrNameTy.SW,
                    rs2=self.__regGen(),
                    rs1=base,
                    imm=addr_offset,
                ),
            ]
            + self.generateBB()
            + gen_preambula()
            + [
                instr.Instruction(
                    isa.info.InstrNameTy.LW,
                    rd=self.__regGen(),
                    rs1=base,
                    imm=addr_offset,
                ),
            ]
        )

        return instr_stream

    def generateBB(self, instrs_count: int = 10) -> list[instr.Instruction]:
        instr_set = list(isa.info.InstrNameTy)
        for name, fmt in isa.info.NAME_TO_FORMAT.items():
            if fmt in (isa.info.InstrFormatTy.J, isa.info.InstrFormatTy.B):
                instr_set.remove(name)

        ignored_categories = [
            isa.info.InstrCategoryTy.SYS,
            isa.info.InstrCategoryTy.LOAD,
            isa.info.InstrCategoryTy.STORE,
        ]

        for instr_category in ignored_categories:
            for name in isa.info.CATEGORY_TO_INSTR[instr_category]:
                instr_set.remove(name)

        return list(
            map(
                lambda _: self.generateInstr(instr_set),
                range(instrs_count),
            )
        )

    def genetateAsm(self, instr_data: instr.Instruction):
        cur_format: InstrFormatTy = isa.info.NAME_TO_FORMAT.get(instr_data.name)
        mnemonic = f"{instr_data.name.name}"

        match cur_format:
            case InstrFormatTy.R:
                asm_str = "{} x{}, x{}, x{}".format(
                    mnemonic, instr_data.rd, instr_data.rs1, instr_data.rs2
                )
            #
            case InstrFormatTy.I:
                res_imm: str = map_imm(instr_data.imm, 12, IMM_DICT["imm12"])

                if instr_data.name in isa.info.CATEGORY_TO_INSTR[InstrCategoryTy.LOAD]:
                    asm_str = "{} x{}, {}(x{})".format(
                        mnemonic, instr_data.rd, res_imm, instr_data.rs1
                    )
                else:
                    asm_str = "{} x{}, x{}, {}".format(
                        mnemonic, instr_data.rd, instr_data.rs1, hex(res_imm)
                    )
            #
            case InstrFormatTy.S:
                res_imm: str = map_imm(
                    instr_data.imm, 12, IMM_DICT["imm12lo"], IMM_DICT["imm12hi"]
                )

                if instr_data.name in isa.info.CATEGORY_TO_INSTR[InstrCategoryTy.STORE]:
                    asm_str = "{} x{}, {}(x{})".format(
                        mnemonic, instr_data.rs2, res_imm, instr_data.rs1
                    )
                else:
                    asm_str = "{} x{}, x{}, {}".format(
                        mnemonic, instr_data.rs1, instr_data.rs2, hex(res_imm)
                    )
            #
            case InstrFormatTy.B:
                res_imm: str = map_imm(
                    instr_data.imm, 12, IMM_DICT["bimm12lo"], IMM_DICT["bimm12hi"]
                )

                asm_str = "{} x{}, x{}, {}".format(
                    mnemonic, instr_data.rs1, instr_data.rs2, hex(res_imm)
                )
            #
            case InstrFormatTy.U:
                res_imm: str = map_imm(instr_data.imm, False, IMM_DICT["imm20"])

                asm_str = "{} x{}, {}".format(mnemonic, instr_data.rd, hex(res_imm))
            #
            case InstrFormatTy.J:
                res_imm: str = map_imm(instr_data.imm, 20, IMM_DICT["jimm20"])

                asm_str = "{} x{}, {}".format(mnemonic, instr_data.rd, hex(res_imm))
            #
            case _:
                if instr_data.name in isa.info.CATEGORY_TO_INSTR[InstrCategoryTy.SYS]:
                    pass
                else:
                    raise RuntimeError(
                        f"Error : there is no support instruction {mnemonic}"
                    )

        return asm_str.lower()


def ones(num: int):
    return (1 << num) - 1


def get_mask(msb: int, lsb: int) -> int:
    return ones(msb - lsb + 1) << lsb


def get_bits(value: int, msb: int, lsb: int):
    assert msb >= lsb
    return (value) & get_mask(msb, lsb)


def sext(value, nbits=32):
    sign_bit = 1 << (nbits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)


def map_imm(value: int, nbits: int, *imm_dicts):
    mapped, imm_shift = 0, None
    do_sext = False
    #
    for imm_dict in imm_dicts:
        for it in reversed(imm_dict):
            imm_shift = it["lsb"] if imm_shift == None else imm_shift
            #
            width, bits = it["msb"] - it["lsb"] + 1, get_bits(
                value, it["msb"], it["lsb"]
            )
            mapped |= bits >> it["lsb"]
            #
            imm_shift += width

            if it["msb"] == 31 and nbits:
                do_sext = (bits >> 31) & (1)
    #
    return mapped if not do_sext else sext(mapped, nbits)
