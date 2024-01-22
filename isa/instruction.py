from dataclasses import dataclass
import random

from isa.info import InstrNameTy


@dataclass
class FieldPart:
    lsb: int
    msb: int
    shamt: int


@dataclass
class Field:
    pass


@dataclass
class Instruction:
    name: InstrNameTy

    rd: int
    rs1: int
    rs2: int
    rs3: int
    imm: int
