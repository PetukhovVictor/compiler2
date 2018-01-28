from .Core.registers import Registers
from .Core.types import *

""" Map: arithmetic operator in programming language = arithmetic operator in ASM """
binop_compare_map = {
    '+': {
        'operator': Commands.ADD,
        'operands': [Registers.EAX, Registers.EBX]
    },
    '-': {
        'operator': Commands.SUB,
        'operands': [Registers.EAX, Registers.EBX]
    },
    '*': {
        'operator': Commands.MUL,
        'operands': [Registers.EBX]
    },
    '/': {
        'operator': Commands.IDIV,
        'operands': [Registers.EBX]
    },
    '%': {
        'operator': Commands.IDIV,
        'operands': [Registers.EBX]
    }
}


def int_aexp(compiler, i):
    """ Integer compilation """
    compiler.code.add(Commands.MOV, [Registers.EAX, i])\
        .add(Commands.PUSH, Registers.EAX)

    return compiler.types.set(Types.INT)


def binop_aexp(compiler, op, left, right):
    """ Arithmetic expression compilation """
    left.compile_asm(compiler)
    compiler.types.pop()
    right.compile_asm(compiler)
    compiler.types.pop()
    compiler.code.add(Commands.POP, Registers.EBX)\
        .add(Commands.POP, Registers.EAX)

    if op == '/' or op == '%':
        compiler.code.add(Commands.CDQ)

    compiler.code.add(binop_compare_map[op]['operator'], binop_compare_map[op]['operands'])

    if op == '%':
        compiler.code.add(Commands.MOV, [Registers.EAX, Registers.EDX])

    compiler.code.add(Commands.PUSH, Registers.EAX)

    return compiler.types.set(Types.INT)


def var_aexp(compiler, name, context, value_type):
    """ Variable compilation """
    if context == 'assign':
        var = compiler.environment.add_local_var(value_type, name)
        compiler.code.add(Commands.POP, var)
    else:
        compiler.code.add(Commands.MOV, [Registers.EAX, compiler.environment.get_local_var(name)])\
            .add(Commands.PUSH, Registers.EAX)
        var_type = compiler.environment.get_local_var_type(name)

        return compiler.types.set(var_type)
