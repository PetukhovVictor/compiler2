from pprint import pprint

from ..types import *

typesMap = {
    Types.STRING: lambda scope: scope.heap,
    Types.STRING_INLINE: lambda scope: scope.stack,
    Types.UNBOXED_ARR: lambda scope: scope.heap,
    Types.UNBOXED_ARR_INLINE: lambda scope: scope.stack
}

class Clonner:
    @staticmethod
    def string(pointer, stack, string_type, source, target):
        heap_offset = pointer
        current_symbol = None
        start_pointer = len(target.heap)
        while current_symbol != 0:
            current_symbol = typesMap[string_type](source)[heap_offset]
            target.heap.append(current_symbol)
            heap_offset += 1
        stack.append(Types.STRING)
        stack.append(start_pointer)

    @staticmethod
    def unboxed_array(pointer, stack, string_type, source, target):
        arrlen = typesMap[string_type](source)[pointer]
        start_pointer = len(target.heap)
        arr_counter = 0
        while arr_counter <= arrlen:
            current_symbol = typesMap[string_type](source)[pointer + arr_counter]
            target.heap.append(current_symbol)
            arr_counter += 1
        stack.append(Types.UNBOXED_ARR)
        stack.append(start_pointer)

    @staticmethod
    def clone(pointer, stack, object_type, source, target):
        if object_type == Types.STRING or object_type == Types.STRING_INLINE:
            Clonner.string(pointer, stack, object_type, source, target)
        else:
            Clonner.unboxed_array(pointer, stack, object_type, source, target)
