from __future__ import annotations

import ast
from types import resolve_bases

from python.analysis import name_resolution
from python.analysis.name_resolution import (
    BindingTable,
    NameType,
    get_declaration,
    get_name_type,
    is_declaration,
)
from python.analysis.parse_types import type_of_annotation
from python.analysis.ptypes.py_builtins import (
    UnknownType,
    builtin_bool,
    builtin_float,
    builtin_int,
    builtin_str,
    builtins_map,
)
from python.analysis.ptypes.py_list import ListType
from python.analysis.ptypes.py_tuple import TupleType
from python.analysis.py_types import (
    ClassType,
    FunctionType,
    IteratorType,
    MethodType,
    PyType,
    RangeType,
    TypeTable,
    builtin_funcs,
    get_attribute_type,
    get_call_type,
    resolve_builtin,
)
from python.analysis.scope import ScopingNodeVisitor
from python.errors import PyToCppError
from python.formatting import get_type_name
from python.utils import dump


class TypeInferrer(ScopingNodeVisitor):
    def __init__(self, node_scopes, bindings: BindingTable, types: TypeTable):
        super().__init__(node_scopes)
        self.bindings = bindings
        self.types = types
        # A stack of classes being visited
        self.current_class = []

    def type_of(self, operand) -> PyType:
        """Normalize a node-or-type argument to its PyType."""
        if isinstance(operand, ast.AST):
            return self.types[operand]
        return operand  # already a PyType

    def type_check(self, a, b) -> None:
        type_a = self.type_of(a)
        type_b = self.type_of(b)
        if not self.compatible(type_a, type_b):
            raise PyToCppError(
                a,
                f"type mismatch: {get_type_name(type_a)} is not compatible with {get_type_name(type_b)}",
            )

    def compatible(self, source: PyType, target: PyType) -> bool:
        if isinstance(source, UnknownType) or isinstance(target, UnknownType):
            return True
        if source is target:
            return True
        if source == builtin_bool:
            if target == builtin_int or target == builtin_float:
                return True
        if source == builtin_int and target == builtin_float:
            return True
        if isinstance(source, ListType) and isinstance(target, ListType):
            if isinstance(source.element_type, UnknownType) or isinstance(
                source.element_type, UnknownType
            ):
                return True
        return False

    def is_attributable(self, typ: PyType):
        return isinstance(typ, ClassType)

    def visit_Name(self, node: ast.Name):
        # This name can't be an annotation
        name_type = get_name_type(node, self.bindings)
        match name_type:
            case NameType.reference:
                type = self.types[get_declaration(node, self.bindings)]
            case NameType.declaration:
                type = UnknownType()
            case NameType.builtin:
                type = resolve_builtin(node.id)
        self.types[node] = type

    def visit_Constant(self, node: ast.Constant):
        if node.value is None:
            typ = builtins_map["None"]
        else:
            typ = builtins_map[type(node.value).__name__]
        self.types[node] = typ

    def visit_Assign(self, node: ast.Assign):
        self.visit(node.targets)
        self.visit(node.value)
        for target in node.targets:
            self.type_check(target, self.types[node.value])
            if target not in self.types or isinstance(self.types[target], UnknownType):
                # We take this oppurtinity to bind this variable to the inferred type
                self.types[target] = self.types[node.value]

    def visit_AnnAssign(self, node: ast.AnnAssign):
        annotation_type = type_of_annotation(node.annotation, self.bindings, self.types)
        self.visit(node.target)
        self.type_check(node.target, annotation_type)
        if node.value is not None:
            self.visit(node.value)
            self.type_check(node.value, annotation_type)
        self.types[node.target] = annotation_type
        if node.value is not None:
            self.types[node.value] = annotation_type

    def visit_ClassDef(self, node: ast.ClassDef):
        typ = self.types[node]
        # We keep track of wether we are in a class and which class for handling self in function definitions
        self.current_class.append(typ)
        self.visit(node.body)
        self.current_class.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.visit(node.args)
        self.visit(node.body)

    def visit_For(self, node: ast.For):
        self.visit(node.target)
        self.visit(node.iter)
        iter_type = self.types[node.iter]
        if isinstance(iter_type, ListType):
            self.types[node.target] = iter_type.element_type
        elif isinstance(iter_type, IteratorType):
            self.types[node.target] = iter_type.element_type
        elif isinstance(iter_type, RangeType):
            self.types[node.target] = builtin_int
        self.visit(node.body)

    def visit_Call(self, node: ast.Call):
        self.visit(node.func)
        self.visit(node.args)
        base_type = self.types[node.func]
        self.types[node] = get_call_type(base_type)

    def visit_arguments(self, node: ast.arguments):
        starting_argument = 0
        if self.current_class:
            cls = self.current_class[-1]
            assert len(node.args) >= 1
            self.types[node.args[0]] = cls
            starting_argument = 1
        for arg in node.args[starting_argument:]:
            self.visit(arg)

    def visit_arg(self, node: ast.arg):
        assert node.annotation is not None
        annotation_type = type_of_annotation(node.annotation, self.bindings, self.types)
        self.types[node] = annotation_type

    def visit_Attribute(self, node: ast.Attribute):
        self.visit(node.value)
        base_type = self.types[node.value]
        self.types[node] = get_attribute_type(base_type, node.attr)

    def visit_List(self, node: ast.List):
        for element in node.elts:
            self.visit(element)
        if len(node.elts) == 0:
            self.types[node] = ListType(UnknownType())
            return
        element_type = self.types[node.elts[0]]
        for element in node.elts:
            self.type_check(element, element_type)
        self.types[node] = ListType(element_type)

    def visit_Tuple(self, node: ast.Tuple):
        for element in node.elts:
            self.visit(element)
        types = [self.types[element] for element in node.elts]
        self.types[node] = TupleType(types)

    def visit_Subscript(self, node: ast.Subscript):
        # Slices always return the container type
        # Assuming that tuples aren't sliced
        self.visit(node.value)
        self.visit(node.slice)
        base_type = self.types[node.value]
        if isinstance(node.slice, ast.Slice):
            self.types[node] = base_type
            return
        assert isinstance(base_type, ClassType)
        assert base_type.get_item_type is not None
        self.types[node] = base_type.get_item_type

    def visit_BinOp(self, node: ast.BinOp):
        self.visit(node.left)
        self.visit(node.right)
        left_type = self.types[node.left]
        right_type = self.types[node.right]
        typ = self.binop_type(node.op, left_type, right_type)
        self.types[node] = typ

    def visit_UnaryOp(self, node: ast.UnaryOp):
        self.visit(node.operand)
        operand_type = self.types[node.operand]
        numeric = (builtin_bool, builtin_int, builtin_float)

        match node.op:
            # not x  ->  always bool, for any operand
            case ast.Not():
                typ = builtin_bool
            # +x / -x  ->  numeric; bool collapses to int (-True == -1)
            case ast.UAdd() | ast.USub():
                assert operand_type in numeric, f"unary +/- on {operand_type}"
                typ = builtin_int if operand_type is builtin_bool else operand_type
            # ~x  ->  integer bitwise invert; not valid on float
            case ast.Invert():
                assert operand_type in (
                    builtin_bool,
                    builtin_int,
                ), f"unary ~ on {operand_type}"
                typ = builtin_int
            case _:
                assert False, f"unsupported UnaryOp {type(node.op).__name__}"

        self.types[node] = typ

    def visit_AugAssign(self, node: ast.AugAssign):
        self.visit(node.target)
        self.visit(node.value)
        target_type = self.types[node.target]
        value_type = self.types[node.value]
        result_type = self.binop_type(node.op, target_type, value_type)

        # static typing: the variable's type must not change
        if result_type is not target_type:
            raise ValueError(
                f"{dump(node.target)} on line {node.lineno} is {target_type} "
                f"but {type(node.op).__name__} with {value_type} yields {result_type}"
            )

        self.types[node] = target_type

    def visit_BoolOp(self, node: ast.BoolOp):
        # and/or evaluate to one of their operands
        for value in node.values:
            self.visit(value)
        operand_types = [self.types[value] for value in node.values]
        first = operand_types[0]
        assert all(
            t is first for t in operand_types
        ), f"mixed BoolOp operand types on line {node.lineno}: {operand_types}"
        self.types[node] = first

    def visit_Compare(self, node: ast.Compare):
        self.visit(node.left)
        for comparator in node.comparators:
            self.visit(comparator)
        self.types[node] = builtin_bool

    def binop_type(self, op: ast.operator, left: PyType, right: PyType) -> PyType:
        def numeric_rank(type: PyType) -> int | None:
            if type == builtin_bool:
                return 0
            if type == builtin_int:
                return 1
            if type == builtin_float:
                return 2
            return None

        both_numeric = (
            numeric_rank(left) is not None and numeric_rank(right) is not None
        )

        def widen(left: PyType, right: PyType) -> PyType:
            rank_left = numeric_rank(left)
            rank_right = numeric_rank(right)
            assert rank_left is not None
            assert rank_right is not None
            wider = left if rank_left >= rank_right else right
            # bool collapses to int under arithmetic (1 + True == 2)
            return builtin_int if wider is builtin_bool else wider

        # True division always yields float for numerics
        if isinstance(op, ast.Div):
            assert both_numeric, f"unsupported / on {left} and {right}"
            return builtin_float

        # Bitwise / shift: integers only (bool counts as int) -> int
        if isinstance(op, (ast.LShift, ast.RShift, ast.BitOr, ast.BitAnd, ast.BitXor)):
            ints = (builtin_bool, builtin_int)
            assert (
                left in ints and right in ints
            ), f"unsupported {type(op).__name__} on {left} and {right}"
            return builtin_int

        # Arithmetic on numerics: widen, bool -> int
        if (
            isinstance(op, (ast.Add, ast.Sub, ast.Mult, ast.FloorDiv, ast.Mod, ast.Pow))
            and both_numeric
        ):
            return widen(left, right)

        # str concatenation
        if isinstance(op, ast.Add) and left is builtin_str and right is builtin_str:
            return builtin_str

        # str repetition: str * int  or  int * str
        if isinstance(op, ast.Mult) and (
            (left is builtin_str and right in (builtin_bool, builtin_int))
            or (right is builtin_str and left in (builtin_bool, builtin_int))
        ):
            return builtin_str

        assert False, f"unsupported BinOp {type(op).__name__} on {left} and {right}"
