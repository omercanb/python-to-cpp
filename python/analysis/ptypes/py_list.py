from dataclasses import dataclass

from python.analysis.ptypes.py_builtins import (
    ContainerType,
    PyType,
    builtin_int,
    builtin_none,
)


# Gives the return type of a method call
class ListType(ContainerType):
    def __init__(self, element_type):
        self.name = "list"
        self.element_type = element_type

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
