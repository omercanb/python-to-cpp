from __future__ import annotations

import builtins
from dataclasses import dataclass


class PyType:
    pass


class ContainerType(PyType):
    pass


# Used for empty containers like []
class UnknownType(PyType):
    pass


@dataclass
class BuiltinType(PyType):
    name: str


builtins_map = {
    builtin_name: BuiltinType(builtin_name) for builtin_name in dir(builtins)
}
builtin_int = builtins_map["int"]
builtin_float = builtins_map["float"]
builtin_bool = builtins_map["bool"]
builtin_str = builtins_map["str"]
builtin_none = builtins_map["None"]
unkown_type = UnknownType()
