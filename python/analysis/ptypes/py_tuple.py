from python.analysis.ptypes.py_builtins import ContainerType
from python.analysis.py_types import PyType


class TupleType(ContainerType):
    def __init__(self, element_types: list[PyType]):
        self.name = "tuple"
        self.element_types: list[PyType] = element_types

    def __getitem__(self, i: int | None) -> PyType:
        if i is not None:
            return self.element_types[i]
        else:
            raise NotImplementedError("Can't convert an unkown tuple access")
