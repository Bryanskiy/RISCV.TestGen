import isa.instruction as instr
from enum import Enum
import random
from dataclasses import dataclass
from typing import Sequence

import isa.info


@dataclass
class GenCfg:
    mem_instrs_allowed: bool = False
    instrs_count: int = 10


@dataclass
class Generator:
    seed: int = 0

    def generateInstrNamed(self, name: isa.info.InstrNameTy) -> instr.Instruction:
        def randgen(bound: int):
            return random.randint(0, bound - 1)

        def regGen():
            return randgen(1 << 5)

        return instr.Instruction(
            name,
            regGen(),
            regGen(),
            regGen(),
            regGen(),
            randgen(1 << isa.info.XLEN),
        )

    def generateInstr(self, allowed: Sequence[isa.info.InstrNameTy]):
        random.seed(self.seed)
        name = isa.info.InstrNameTy(random.choice(allowed))

        def randgen(bound: int):
            return random.randint(0, bound - 1)

        def regGen():
            return randgen(1 << 5)

        return instr.Instruction(
            name,
            regGen(),
            regGen(),
            regGen(),
            regGen(),
            randgen(1 << isa.info.XLEN),
        )

    def generateBB(self, cfg: GenCfg = GenCfg()) -> list[instr.Instruction]:
        instr_set = list(isa.info.InstrNameTy)
        for name, fmt in isa.info.NAME_TO_FORMAT.items():
            if fmt in (isa.info.InstrFormatTy.J, isa.info.InstrFormatTy.B):
                instr_set.remove(name)

        ignored_categories = [
            isa.info.InstrCategoryTy.SYS,
        ]
        if cfg.mem_instrs_allowed:
            ignored_categories.extend(
                (
                    isa.info.InstrCategoryTy.LOAD,
                    isa.info.InstrCategoryTy.STORE,
                )
            )

        for instr_category in ignored_categories:
            for name in isa.info.CATEGORY_TO_INSTR[instr_category]:
                instr_set.remove(name)

        ret = list(
            map(
                lambda _: instr_set[random.randint(0, cfg.instrs_count - 1)],
                range(cfg.instrs_count),
            )
        )
        return ret
