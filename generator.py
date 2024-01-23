import isa.instruction as instr
from enum import Enum
import random
from dataclasses import dataclass
from typing import Sequence, ClassVar

import isa.info


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
                lambda _: random.choice(instr_set),
                range(instrs_count),
            )
        )
