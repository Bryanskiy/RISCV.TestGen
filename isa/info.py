from enum import Enum, IntEnum, auto
from typing import Any, TypeAlias
from collections import defaultdict

from dataclasses import dataclass

# https://github.com/llvm-mirror/llvm/blob/master/lib/Target/RISCV/RISCVInstrFormats.td
class InstrFormatTy(IntEnum):
    R = 0
    I = auto()
    S = auto()
    B = auto()
    U = auto()
    J = auto()


XLEN = 32


InstrNameTy: TypeAlias = Any
InstrCategoryTy : dict = {}
BitDict = dict[str, bool | int]


class InstrCategoryTy(IntEnum):
    LOAD = 0
    STORE = auto()
    SYS = auto()


CATEGORY_TO_INSTR: dict = {}

NAME_TO_FORMAT: dict[InstrNameTy, InstrFormatTy] = {}
FORMAT_TO_INSTR: dict[InstrFormatTy, set[InstrNameTy]] = defaultdict(set)
FORMAT_TO_FIELDS = {
    InstrFormatTy.R: (
        {"rd", "rs1", "rs2"},
        {"rd", "rs1", "rs2", "rs3"},
    ),
    InstrFormatTy.I: ({"rd", "rs1", "imm12"},),
    InstrFormatTy.S: ({"imm12lo", "rs1", "rs2", "imm12hi"},),
    InstrFormatTy.B: ({"bimm12lo", "rs1", "rs2", "bimm12hi"},),
    InstrFormatTy.U: ({"rd", "imm20"},),
    InstrFormatTy.J: ({"rd", "jimm20"},),
}

def get_bit_map_dict(
    msb: int, lsb: int | None = None, lshift: int = 0, signext: bool = True) -> BitDict:
    """Helper function to build decoding dictionary"""

    if lsb is None:
        lsb = msb
    assert msb >= lsb
    assert lshift < 32
    return {
        "msb": msb,
        "lsb": lsb,
        "lshift": lshift,
        "from": lshift + msb - lsb,
        "sign": signext,
    }

IMM_DICT: dict[str, tuple[BitDict, ...]] = {
    "imm20": (get_bit_map_dict(31, 12, 12),),
    "jimm20": (
        get_bit_map_dict(31, lshift=20),
        get_bit_map_dict(30, 21, 1),
        get_bit_map_dict(20, lshift=11),
        get_bit_map_dict(19, 12, 12),
    ),
    "succ": (get_bit_map_dict(23, 20),),
    "pred": (get_bit_map_dict(27, 24, 4),),
    "fm": (get_bit_map_dict(31, 28, 8),),
    "imm12": (get_bit_map_dict(31, 20),),
    "zimm": (get_bit_map_dict(19, 15, signext=False),),
    "aq": (get_bit_map_dict(26, lshift=1),),
    "rl": (get_bit_map_dict(25),),
    "bimm12hi": (
        get_bit_map_dict(31, lshift=12),
        get_bit_map_dict(30, 25, 5),
    ),
    "bimm12lo": (
        get_bit_map_dict(11, 8, 1),
        get_bit_map_dict(7, lshift=11),
    ),
    "imm12hi": (get_bit_map_dict(31, 25, 5),),
    "imm12lo": (get_bit_map_dict(11, 7),),
    "shamtw": (get_bit_map_dict(24, 20),),
}

def generate_enums(yaml_dict: dict[str, Any]):
    extensions: set[str] = set()
    instructions: list[str] = []
    name_to_format: dict[str, InstrFormatTy] = {}

    for name, data in yaml_dict.items():
        for ext in data["extension"]:
            extensions.add(ext)

        instructions.append(name.upper())

        flds = set(data["variable_fields"])

        for fmt, fields in FORMAT_TO_FIELDS.items():
            for field in fields:
                if set(field) == flds:
                    name_to_format[name.upper()] = fmt

    globals()["InstrNameTy"] = Enum("InstrNameTy", instructions, start=0)
    globals()["InstrExtensionTy"] = Enum("InstrExtensionTy", list(extensions), start=0)

    for name, fmt in name_to_format.items():
        NAME_TO_FORMAT[InstrNameTy[name]] = fmt

        FORMAT_TO_INSTR[fmt].add(InstrNameTy[name])

    CATEGORY_TO_INSTR[InstrCategoryTy.LOAD] = (
        InstrNameTy.LB,
        InstrNameTy.LBU,
        InstrNameTy.LH,
        InstrNameTy.LHU,
        InstrNameTy.LW,
    )

    CATEGORY_TO_INSTR[InstrCategoryTy.STORE] = (
        InstrNameTy.SB,
        InstrNameTy.SH,
        InstrNameTy.SW,
    )

    CATEGORY_TO_INSTR[InstrCategoryTy.SYS] = (
        InstrNameTy.ECALL,
        InstrNameTy.EBREAK,
        InstrNameTy.FENCE,
    )
