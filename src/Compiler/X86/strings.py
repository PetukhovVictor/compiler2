# -*- coding: utf-8 -*-

from .Deep.strings import *


def char(compiler, character, need_typify=True, address=None):
    """ Компиляция выражения "символ" """
    if address:
        compiler.code.add('mov', ['byte [%s]' % address, ord(character)])
    else:
        compiler.code.add('push', [ord(character)])
    if need_typify:
        return compiler.commands.set_and_return_type(Types.CHAR)


def string(compiler, characters):
    """ Компиляция выражения "строка" """
    str_length = len(characters)
    str_pointer = compiler.bss.vars.add(None, 'resb', str_length + 2, Types.INT)

    for i, character in enumerate(characters):
        char(compiler, character, need_typify=False, address="%s+%d" % (str_pointer, i))

    compiler.code.add('mov', ['byte [%s+%d]' % (str_pointer, str_length), 0])
    compiler.code.add('push', [str_pointer])

    return compiler.commands.set_and_return_type(Types.STRING)


def strlen(compiler, args):
    """ Компиляция built-in функции strlen (длина строки) """
    array_type = args.elements[0].compile_x86(compiler)
    compiler.commands.clean_type()

    StringCompiler.strlen(compiler, array_type)

    return compiler.commands.set_and_return_type(Types.INT)


def strget(compiler, args):
    """ Компиляция built-in функции strget (получение символа строки) """
    # Порядок компиляции аргументов здесь и ниже задаём удобным для дальнейшей работы образом
    args.elements[1].compile_x86(compiler)
    compiler.commands.clean_type()
    array_type = args.elements[0].compile_x86(compiler)
    compiler.commands.clean_type()
    StringCompiler.strget(compiler, array_type)

    return compiler.commands.set_and_return_type(Types.CHAR)


def strset(compiler, args):
    """ Компиляция built-in функции strset (задание символа строки) """
    args.elements[2].compile_x86(compiler)
    compiler.commands.clean_type()
    args.elements[1].compile_x86(compiler)
    compiler.commands.clean_type()
    array_type = args.elements[0].compile_x86(compiler)
    compiler.commands.clean_type()
    StringCompiler.strset(compiler, array_type)


def strsub(compiler, args):
    """ Компиляция built-in функции strsub (взятие подстроки строки) """
    args.elements[1].compile_x86(compiler)
    compiler.commands.clean_type()
    array_type = args.elements[0].compile_x86(compiler)
    compiler.commands.clean_type()
    args.elements[2].compile_x86(compiler)
    compiler.commands.clean_type()
    StringCompiler.strsub(compiler, array_type)

    return compiler.commands.set_and_return_type(Types.STRING)


def strdup(compiler, args):
    """ Компиляция built-in функции strdup (дублирование строки) """
    array_type = args.elements[0].compile_x86(compiler)
    compiler.commands.clean_type()
    StringCompiler.strdup(compiler, array_type)

    return compiler.commands.set_and_return_type(Types.STRING)
