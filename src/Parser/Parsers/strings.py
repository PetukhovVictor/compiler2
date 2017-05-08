from src.Parser.Parsers.basic import *

from src.Parser.AST.strings import *

string_predefined_functions = {
    'strlen': StrLen,
    'strget': StrGet,
    'strsub': StrSub,
    'strdup': StrDup,
    'strset': StrSet,
    'strcat': StrCat,
    'strcmp': StrCmp,
    'strmake': StrMake
}

"""
Main arithmetic expressions parser.
"""
def str_exp():
    return Tag(STRING) ^ String
