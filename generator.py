import isa.instruction as instr

from itertools import repeat
from isa.instruction import Instr

class Generator:
    def __init__(self):
        pass

    def generate(self):
        l = []
        l.extend([instr.generate() for i in range(100)])
        return l
