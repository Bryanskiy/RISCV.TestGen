import isa.instruction as instr
from enum import Enum
import random
from dataclasses import dataclass
from typing import Sequence, ClassVar

import isa.info

from itertools import repeat
from isa.info import InstrFormatTy

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
        random.seed(self.seed)
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

    @staticmethod
    def __randgen(bound: int):
        return random.randint(0, bound - 1)

    @staticmethod
    def __regGen():
        return Generator.__randgen(1 << 5)

    def generateInstr(self, allowed: Sequence[isa.info.InstrNameTy]):
        random.seed(self.seed)
        name = isa.info.InstrNameTy(random.choice(allowed))

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
                    isa.info.InstrNameTy.SB,
                    rs2=self.__regGen(),
                    rs1=base,
                    imm=addr_offset,
                ),
            ]
            + self.generateBB()
            + gen_preambula()
            + [
                instr.Instruction(
                    isa.info.InstrNameTy.LB,
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
                lambda _: random.choice(instr_set),
                range(instrs_count),
            )
        )

    def genetateAsm(self, instr_data: instr.Instruction):
        cur_format: InstrFormatTy = isa.info.NAME_TO_FORMAT.get(instr_data.name)
        mnemonic, asm_str = f"{instr_data.name.name}", str()

        match cur_format:
            case InstrFormatTy.R:
                asm_str = '{} x{}, x{}, x{}'.format(
                    mnemonic, instr_data.rd, instr_data.rs1, instr_data.rs2)
            #
            case InstrFormatTy.I:
                if mnemonic in isa.info.INSTR_CATEGORY["LOAD_CATEGORY"]:
                    asm_str = '{} x{}, {} (x{})'.format(
                        mnemonic, instr_data.rd, hex(instr_data.imm), instr_data.rs1)
                else:
                    asm_str = '{} x{}, x{}, {}'.format(
                        mnemonic, instr_data.rd, instr_data.rs1, hex(instr_data.imm))
            #
            case InstrFormatTy.S:
                if instr_data.name in isa.info.InstrCategoryTy["STORE"]:
                    asm_str = '{} x{}, {} (x{})'.format(
                        mnemonic, instr_data.rs2, hex(instr_data.imm), instr_data.rs1)
                else:
                    asm_str = '{} x{}, x{}, {}'.format(
                        mnemonic, instr_data.rs1, instr_data.rs2, hex(instr_data.imm))
            #
            case InstrFormatTy.B:
                asm_str = '{} x{}, x{}, {}'.format(
                    mnemonic, instr_data.rs1, instr_data.rs2, hex(instr_data.imm))
            #
            case InstrFormatTy.U:
                asm_str = '{} x{}, {}'.format(
                    mnemonic, instr_data.rd, hex(instr_data.imm))
            #
            case InstrFormatTy.J:
                asm_str = '{} x{}, {}'.format(
                    mnemonic, instr_data.rd, hex(instr_data.imm))
            #
            case _ : print("Error : there is no support assembler of systsem instruction")

        return asm_str.lower()

    def genetateAsm(self, instr_data: instr.Instruction):
        cur_format: InstrFormatTy = isa.info.NAME_TO_FORMAT.get(instr_data.name)
        mnemonic, asm_str = f"{instr_data.name.name}", str()

        match cur_format:
            case InstrFormatTy.R:
                asm_str = '{} x{}, x{}, x{}'.format(
                    mnemonic, instr_data.rd, instr_data.rs1, instr_data.rs2)
            #
            case InstrFormatTy.I:
                if mnemonic in isa.info.INSTR_CATEGORY["LOAD_CATEGORY"]:
                    asm_str = '{} x{}, {} (x{})'.format(
                        mnemonic, instr_data.rd, hex(instr_data.imm), instr_data.rs1)
                else:
                    asm_str = '{} x{}, x{}, {}'.format(
                        mnemonic, instr_data.rd, instr_data.rs1, hex(instr_data.imm))
            #
            case InstrFormatTy.S:
                if mnemonic in isa.info.INSTR_CATEGORY["STORE_CATEGORY"]:
                    asm_str = '{} x{}, {} (x{})'.format(
                        mnemonic, instr_data.rs2, hex(instr_data.imm), instr_data.rs1)
                else:
                    asm_str = '{} x{}, x{}, {}'.format(
                        mnemonic, instr_data.rs1, instr_data.rs2, hex(instr_data.imm))
            #
            case InstrFormatTy.B:
                asm_str = '{} x{}, x{}, {}'.format(
                    mnemonic, instr_data.rs1, instr_data.rs2, hex(instr_data.imm))
            #
            case InstrFormatTy.U:
                asm_str = '{} x{}, {}'.format(
                    mnemonic, instr_data.rd, hex(instr_data.imm))
            #
            case InstrFormatTy.J:
                asm_str = '{} x{}, {}'.format(
                    mnemonic, instr_data.rd, hex(instr_data.imm))
            #
            case _ : print("Error : there is no support assembler of systsem instruction")

        return asm_str.lower()
