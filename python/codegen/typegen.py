from mypy.types import (
    AnyType,
    Instance,
    NoneType,
    TupleType,
    Type,
    UnionType,
    get_proper_type,
)

from python.codegen.builtins import NON_POINTER_TYPES, POINTER_TYPES


def ptr_type(t: str) -> str:
    return f"ptr<{t}>"


def cpp_type(t: Type) -> str:
    type_name = cpp_type_name(t)
    if is_pointer(t):
        type_name = ptr_type(type_name)
    return type_name


def cpp_type_name(t: Type) -> str:
    """Convert a mypy type to C++ type string.

    Uses pattern matching to handle different type kinds.
    """
    t = get_proper_type(t)

    match t:
        # Builtin types
        case Instance(type=type_info) if type_info.fullname == "builtins.int":
            return "_int"
        case Instance(type=type_info) if type_info.fullname == "builtins.float":
            return "_float"
        case Instance(type=type_info) if type_info.fullname == "builtins.str":
            return "std::string"
        case Instance(type=type_info) if type_info.fullname == "builtins.bool":
            return "bool"

        # Container types
        case Instance(type=type_info, args=args) if (
            type_info.fullname == "builtins.list" and args
        ):
            elem_type = cpp_type_name(args[0])
            return f"list<{elem_type}>"

        case Instance(type=type_info, args=args) if (
            type_info.fullname == "builtins.dict" and len(args) >= 2
        ):
            key_type = cpp_type_name(args[0])
            val_type = cpp_type_name(args[1])
            return f"dict<{key_type}, {val_type}>"

        case Instance(type=type_info, args=args) if (
            type_info.fullname == "builtins.set" and args
        ):
            elem_type = cpp_type_name(args[0])
            return f"set<{elem_type}>"

        # Tuple with fixed elements
        case TupleType(items=items):
            elem_types = ", ".join(cpp_type_name(item) for item in items)
            return f"tuple<{elem_types}>"

        # Optional[T] = T | None
        case UnionType(items=items) if len(items) == 2 and any(
            isinstance(item, NoneType) for item in items
        ):
            non_none = next(item for item in items if not isinstance(item, NoneType))
            inner = cpp_type_name(non_none)
            return f"std::optional<{inner}>"

        # Generic union
        case UnionType(items=items):
            types = ", ".join(cpp_type_name(item) for item in items)
            return f"std::variant<{types}>"

        # None/void
        case NoneType():
            return "void"

        # Any type
        case AnyType():
            return "auto"

        case Instance(type=type_info):
            return type_info.name

        # Iterator/Iterable
        case Instance(type=type_info, args=args) if (
            "Iterator" in type_info.fullname and args
        ):
            elem_type = cpp_type_name(args[0])
            return f"Iterator<{elem_type}>"

        # Default fallback
        case _:
            assert False, f"Conversion not implemented for type {t}"


def is_dict(t: Type) -> bool:
    """Returns whether a type is a dict.

    Dict reads and writes generate different C++: d[k] inserts on a missing
    key (the write path), while a read has to raise KeyError instead.
    """
    t = get_proper_type(t)
    return isinstance(t, Instance) and t.type.fullname == "builtins.dict"


def is_pointer(t: Type) -> bool:
    """Returns whether a type is a pointer"""
    t = get_proper_type(t)

    match t:
        # Builtin types
        case Instance(type=type_info):
            if type_info.name in NON_POINTER_TYPES:
                return False
            if type_info.name in POINTER_TYPES:
                return True
            # User defined classes
            return True
        case TupleType():
            return False

        # Optional[T] = T | None
        case UnionType():
            return False
        # None/void
        case NoneType():
            return False

        # Default fallback
        case _:
            assert False, f"Conversion not implemented for type {t}"
