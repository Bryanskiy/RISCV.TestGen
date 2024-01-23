from dataclasses import dataclass
import random

from isa.info import InstrNameTy


@dataclass
class Instruction:
    name: InstrNameTy

    rd: int = 0
    rs1: int = 0
    rs2: int = 0
    rs3: int = 0
    imm: int = 0
