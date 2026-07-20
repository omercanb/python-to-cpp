from mypy.types import Type, get_proper_type, Instance, TupleType, UnionType, NoneType, AnyType


def ptr_type(t: str) -> str:
    return f"ptr<{t}>"


def cpp_type(t: Type) -> str:
    """Convert a mypy type to C++ type string.

    Uses pattern matching to handle different type kinds.
    """
    t = get_proper_type(t)

    match t:
        # Builtin types
        case Instance(type=type_info) if type_info.fullname == "builtins.int":
            return "int"
        case Instance(type=type_info) if type_info.fullname == "builtins.float":
            return "double"
        case Instance(type=type_info) if type_info.fullname == "builtins.str":
            return "std::string"
        case Instance(type=type_info) if type_info.fullname == "builtins.bool":
            return "bool"

        # Container types
        case Instance(type=type_info, args=args) if (
            type_info.fullname == "builtins.list" and args
        ):
            elem_type = cpp_type(args[0])
            return ptr_type(f"list<{elem_type}>")

        case Instance(type=type_info, args=args) if (
            type_info.fullname == "builtins.dict" and len(args) >= 2
        ):
            key_type = cpp_type(args[0])
            val_type = cpp_type(args[1])
            return ptr_type(f"dict<{key_type}, {val_type}>")

        case Instance(type=type_info, args=args) if (
            type_info.fullname == "builtins.set" and args
        ):
            elem_type = cpp_type(args[0])
            return ptr_type(f"set<{elem_type}>")

        # Tuple with fixed elements
        case TupleType(items=items):
            elem_types = ", ".join(cpp_type(item) for item in items)
            return f"tuple<{elem_types}>"

        # Optional[T] = T | None
        case UnionType(items=items) if len(items) == 2 and any(
            isinstance(item, NoneType) for item in items
        ):
            non_none = next(item for item in items if not isinstance(item, NoneType))
            inner = cpp_type(non_none)
            return f"std::optional<{inner}>"

        # Generic union
        case UnionType(items=items):
            types = ", ".join(cpp_type(item) for item in items)
            return f"std::variant<{types}>"

        # None/void
        case NoneType():
            return "void"

        # Any type
        case AnyType():
            return "auto"

        # Custom classes ptr<A>
        case Instance(type=type_info):
            return ptr_type(type_info.name)

        # Iterator/Iterable
        case Instance(type=type_info, args=args) if (
            "Iterator" in type_info.fullname and args
        ):
            elem_type = cpp_type(args[0])
            return f"Iterator<{elem_type}>"

        # Default fallback
        case _:
            assert False, f"Conversion not implemented for type {t}"
