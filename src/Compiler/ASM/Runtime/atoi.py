from .base import Base


class Atoi(Base):
    is_loaded = False

    def __init__(self, compiler):
        Base.__init__(self, compiler)

        if Atoi.is_loaded:
            return

        self.load('atoi.asm', 'atoi')
        Atoi.is_loaded = True
