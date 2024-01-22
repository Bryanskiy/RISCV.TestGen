from dataclasses import dataclass
from isa.info import InstrFormatTy
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
    rd: int
    rs1: int
    rs2: int
    rs3: int
    imm: int

    name: InstrNameTy
