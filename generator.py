import isa.instruction as instr
from enum import Enum
import random

import isa.info


class Generator:
    def __init__(self):
        pass

    def generateInstr(self):
        name = isa.info.InstrNameTy(random.randint(0, len(isa.info.InstrNameTy) - 1))

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
