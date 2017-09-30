from pprint import pprint
import os

from .base import Base

class Itoa(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if self.is_loaded:
            return

        self.load('itoa.asm')
        self.compiler.data.add('_itoa_radix', 'dd', '10')
        self.compiler.bss.add('_char', 'resb', 1)
        self.is_loaded = True
