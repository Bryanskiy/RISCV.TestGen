from enum import Enum, IntEnum, auto
from typing import Any, TypeAlias


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

NAME_TO_FORMAT: dict[InstrNameTy, InstrFormatTy] = {}
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
