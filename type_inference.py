from __future__ import annotations

import ast
from functools import singledispatchmethod

from errors import PyToCppError
from formatting import format_type, get_type_name
from name_resolution import BindingTable
from py_types import (
    ClassType,
    FunctionAndClassTypeTable,
    FunctionType,
    MethodType,
    PyType,
    UnkownType,
    builtin_bool,
    builtin_float,
    builtin_int,
    builtin_str,
    builtins_map,
    parse_class_stub,
    parse_class_type,
    parse_function,
    type_of_annotation,
)
from scope import ScopeType, ScopingNodeVisitor
from utils import dump


# We have to take a two pass approach to first declare the names of the classes as types
class FunctionAndClassTypeAnnotator(ScopingNodeVisitor):
    def __init__(
        self, node_scopes, bindings: BindingTable, types: FunctionAndClassTypeTable
    ):
        super().__init__(node_scopes)
        self.bindings = bindings
        self.types = types

    def visit_FunctionDef(self, node: ast.FunctionDef):
        scope = self.scope_tracker.node_scopes[node]
        if scope.typ == ScopeType.CLASS:
            return
        self.types[node] = parse_function(node, self.bindings, self.types)
        self.visit(node.body)

    def visit_ClassDef(self, node: ast.ClassDef):
        class_type = self.types[node]
        assert isinstance(class_type, ClassType)
        parse_class_type(class_type, self.bindings, self.types)
        self.visit(node.body)


class ClassTypeDeclarer(ScopingNodeVisitor):
    def __init__(self, node_scopes, bindings: BindingTable):
        super().__init__(node_scopes)
        self.bindings = bindings
        self.types: FunctionAndClassTypeTable = {}

    def visit_ClassDef(self, node: ast.ClassDef):
        scope = None
        for stmt in node.body:
            scope = self.node_scopes().get(stmt)
            if scope is not None:
                break
        assert scope is not None
        self.types[node] = parse_class_stub(node, scope, self.node_scopes())
        self.visit(node.body)


class TypeInferrer2(ScopingNodeVisitor):
    def __init__(self, node_scopes, bindings: BindingTable, types):
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
        if isinstance(source, UnkownType) or isinstance(target, UnkownType):
            return True
        if source is target:
            return True
        if source == builtin_bool:
            if target == builtin_int or target == builtin_float:
                return True
        if source == builtin_int and target == builtin_float:
            return True
        return False

    def is_attributable(self, typ: PyType):
        return isinstance(typ, ClassType)

    def visit_Name(self, node: ast.Name):
        if node not in self.bindings:
            typ = UnkownType()
        else:
            binding = self.bindings[node]
            typ = self.types[binding.node]
        self.types[node] = typ

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
            if target not in self.types or isinstance(self.types[target], UnkownType):
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

    def visit_ClassDef(self, node: ast.ClassDef):
        typ = self.types[node]
        # We keep track of wether we are in a class and which class for handling self in function definitions
        self.current_class.append(typ)
        self.visit(node.body)
        self.current_class.pop()

    def visit_Call(self, node: ast.Call):
        self.visit(node.func)
        self.visit(node.args)
        # The function or class type
        base_type = self.types[node.func]
        assert (
            isinstance(base_type, FunctionType)
            or isinstance(base_type, ClassType)
            or isinstance(base_type, MethodType)
        )
        if isinstance(base_type, FunctionType) or isinstance(base_type, MethodType):
            typ = base_type.return_type
        else:
            typ = base_type
        self.types[node] = typ

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
        annotaion_type = type_of_annotation(node.annotation, self.bindings, self.types)
        self.types[node] = annotaion_type

    def visit_Attribute(self, node: ast.Attribute):
        self.visit(node.value)
        base_type = self.types[node.value]
        assert isinstance(base_type, ClassType)
        attribute = node.attr
        cls = base_type

        typ = None
        for method in cls.methods:
            if method.name == attribute:
                typ = method
                break
        if typ is None:
            typ = cls.fields[attribute]
        self.types[node] = typ

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
        numeric_rank = {builtin_bool: 0, builtin_int: 1, builtin_float: 2}
        both_numeric = left in numeric_rank and right in numeric_rank

        def widen(l: PyType, r: PyType) -> PyType:
            wider = l if numeric_rank[l] >= numeric_rank[r] else r
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
