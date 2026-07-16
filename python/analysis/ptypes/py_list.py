from dataclasses import dataclass

from python.analysis.py_types import PyType
from python.analysis.ptypes.py_builtins import builtin_int, builtin_none


# Gives the return type of a method call
@dataclass
class PyList(PyType):
    element_type: PyType

    def append(self, element_type: PyType) -> PyType:
        return builtin_none

    def pop(self) -> PyType:
        return self.element_type

    def extend(self) -> PyType:
        return builtin_none

    def insert(self) -> PyType:
        return builtin_none

    def remove(self) -> PyType:
        return builtin_none

    def index(self) -> PyType:
        return builtin_int

    def count(self) -> PyType:
        return builtin_int

    def clear(self) -> PyType:
        return builtin_none

    def copy(self) -> PyType:
        return self

    def reverse(self) -> PyType:
        return builtin_none

    def sort(self) -> PyType:
        return builtin_none

    def __getitem__(self) -> PyType:
        return self.element_type
