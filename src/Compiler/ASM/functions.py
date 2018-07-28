# -*- coding: utf-8 -*-

from .Core.registers import Registers
from .Core.config import FUNCTIONS_LABEL_PREFIX
from .Core.types import *
from .Runtime.gc import GC

from .Deep.functions import return_function


def function(compiler, name, args, body):
    """ Компиляция функций (объявление, вызов, исполнение, возврат к месту вызова) """
    function_number = compiler.environment.start(name)
    finish_function = compiler.labels.create()
    function_start_place = compiler.code.get_current_place() + 4

    # При последовательном выполнении пропускаем выполнение тела функции,
    # т. к. в этом случае это лишь объвление функции, вызов будет позже
    compiler.code.add(Commands.JMP, finish_function)

    # На эту метку переходим при вызове
    compiler.code.add_label(FUNCTIONS_LABEL_PREFIX + str(function_number))

    compiler.code.add(Commands.PUSH, Registers.EBP)\
        .add(Commands.MOV, [Registers.EBP, Registers.ESP])

    # Привязываем мапу аргументов с их порядковыми номерами к метке функции
    args_map = {k: v for v, k in enumerate(reversed(args.elements))}
    compiler.environment.set_args(args_map)

    # Компилируем код тела функции
    body.compile_asm(compiler)

    return_type = compiler.environment.get_return_type(name)

    if not return_type:
        compiler.types.set(Types.NOTHING)
        return_function(compiler, args_map)

    compiler.code.add_label(finish_function)

    need_memory = compiler.environment.finish()
    compiler.code.allocate_stack_memory(need_memory, function_start_place)


def return_statement(compiler, expr):
    """ Компиляция выражения возврата к месту вызова """
    args = compiler.environment.get_args()
    return_type = expr.compile_asm(compiler)
    compiler.environment.set_return_type(return_type)

    compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s + 4]' % Registers.ESP])
    compiler.code.add(Commands.MOV, [Registers.EBX, 'dword [%s]' % Registers.ESP])
    GC(compiler).increment()

    return_function(compiler, args)


def call_statement(compiler, name, args):
    """ Компиляция выражения вызова функции """
    for arg in args.elements:
        arg.compile_asm(compiler)
        compiler.code.add(Commands.MOV, [Registers.EBX, 'dword [%s]' % Registers.ESP])
        compiler.code.add(Commands.MOV, [Registers.EAX, 'dword [%s + 4]' % Registers.ESP])
        GC(compiler).increment()

    function_number = compiler.environment.get_number(name)
    compiler.code.add(Commands.CALL, FUNCTIONS_LABEL_PREFIX + str(function_number))

    compiler.code.add(Commands.PUSH, Registers.EAX)
    compile_time_type = compiler.environment.get_return_type(name)

    return compiler.types.set(compile_time_type)
