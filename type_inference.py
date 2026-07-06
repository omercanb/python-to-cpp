import ast
import types
import typing
from dataclasses import dataclass, field

import symbols
from scope import ScopeType
from utils import dump


@dataclass
class Scope:
    # kind: str # "module" | "function" | "class"
    parent: "Scope | None" = None
    names: dict[str, type] = field(default_factory=dict)

    def lookup(self, name: str) -> type | None:
        scope = self
        while scope is not None:
            if name in scope.names:
                return scope.names[name]
            scope = scope.parent
        return None

    def define(self, name: str, t: type) -> None:
        self.names[name] = t


py_builtins = set(["print"])
builtin_types = {"print": typing.Callable[..., None]}


# Used for empty containers like []
class Unkown:
    pass


# A basic type inference walker that will be changed later
# All the visit functions return python types
class TypeInferrer(ast.NodeVisitor):
    types: dict[ast.AST, type] = {}
    scope: Scope = Scope()
    current_scope_type = ScopeType.MODULE
    prev_scope_type = None

    def new_scope_type(self, scope_type: ScopeType):
        self.prev_scope_type = self.current_scope_type
        self.current_scope_type = scope_type

    def old_scope_type(self):
        self.current_scope_type = self.prev_scope_type

    # def visit(self, node):
    #     method = 'visit_' + node.__class__.__name__
    #     visitor = getattr(self, method, None)
    #     if visitor is None:
    #         raise ValueError(f"No support for {node}")
    #     return visitor(node)

    def visit_Module(self, node: ast.Module):
        for stmt in node.body:
            self.visit(stmt)

    def visit_Constant(self, node: ast.Constant):
        return type(node.value)

    # Returns a the type of the list element
    def visit_List(self, node: ast.List):
        # An empty list returns an unkown type which should be checked later
        if len(node.elts) == 0:
            return Unkown
        # Check that all elements of a list are of the same type
        assert all(
            self.visit(element) == self.visit(node.elts[0]) for element in node.elts
        )
        typ = list[self.visit(node.elts[0])]
        self.types[node] = typ
        return typ

    # Returns a tuple of the element types
    def visit_Tuple(self, node: ast.Tuple):
        types = []
        for element in node.elts:
            types.append(self.visit(element))
        typ = tuple[*types]
        self.types[node] = typ
        return typ

    def visit_Name(self, node: ast.Name):
        typ = self.scope.lookup(node.id)
        if typ != None:
            self.types[node] = typ
            return typ

        if node.id in py_builtins:
            return builtin_types[node.id]

        # Name not in scope
        self.types[node] = Unkown
        # return Unkown
        raise ValueError(
            f"Variable '{node.id}' on line {node.lineno} used without declaration"
        )

    def visit_Assign(self, node: ast.Assign):
        target = node.targets[0]
        # How to handle unpackign?
        assert isinstance(target, ast.Name)
        name = target.id
        typ = self.scope.lookup(name)
        if typ == None:
            # This is a declaration
            typ = self.visit(node.value)
            self.scope.define(name, typ)
        else:
            # Check that the static typing holds
            assert typ == self.visit(node.value)

        self.types[node] = typ
        self.types[target] = typ

    def visit_AnnAssign(self, node: ast.AnnAssign):
        assert isinstance(node.target, ast.Name)
        target = node.target
        target_t = type_of_annotation(node.annotation)
        self.scope.define(target.id, target_t)
        self.types[node] = target_t
        self.types[node.target] = target_t
        # If no value to assign we trust the annotation and return that type
        if node.value is None:
            return target_t
        value_t = self.visit(node.value)
        if value_t != target_t:
            raise ValueError(
                f"Annotated assignment {dump(node.target)} type {target_t} is different from assigned type {value_t}"
            )
        return target_t

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.new_scope_type(ScopeType.FUNCTION)
        # Create a new scope
        # For each formal parameter
        # Get the type and define the name to the type
        # define the function on the outer scope

        # Collect the function parameters in the function scope
        this_scope = self.scope
        function_scope = Scope(self.scope)
        args = node.args.args
        argument_types: list[type] = (
            []
        )  # Will be used later for the type of the function itself
        for arg in args:
            if not hasattr(arg, "annotation"):
                raise ValueError(
                    f"Parameter '{arg.arg}' for function '{node.name}' on line {node.lineno} does not have a type annotation"
                )
            typ = type_of_annotation(arg.annotation)
            argument_types.append(typ)
            function_scope.define(arg.arg, typ)
        if not hasattr(node, "returns"):
            raise ValueError(
                f"Function '{node.name}' on line {node.lineno} does not have a return type annotation"
            )
        return_type = type_of_annotation(node.returns)
        function_type = typing.Callable[argument_types, return_type]

        # Define the function in the outer scope and move to the function scope
        self.scope.define(node.name, function_type)
        self.scope = function_scope

        self.types[node] = function_type

        # if node.name != 'main': return
        for stmt in node.body:
            self.visit(stmt)

        self.scope = this_scope
        self.old_scope_type()

    def visit_Return(self, node: ast.Return):
        if node.value:
            return self.visit(node.value)

    def visit_Call(self, node: ast.Call):
        function_type = self.visit(node.func)
        return_type = function_type.__args__[-1]
        return return_type

    def visit_Expr(self, node: ast.Expr):
        return self.visit(node.value)

    # Claude generated
    def _binop_type(self, op: ast.operator, left_t: type, right_t: type) -> type:
        numeric_rank = {bool: 0, int: 1, float: 2, complex: 3}

        if (
            isinstance(op, ast.Div)
            and left_t in numeric_rank
            and right_t in numeric_rank
        ):
            return complex if complex in (left_t, right_t) else float
        if left_t in numeric_rank and right_t in numeric_rank:
            wider = left_t if numeric_rank[left_t] >= numeric_rank[right_t] else right_t
            return int if wider is bool else wider
        if isinstance(op, ast.Add) and left_t == right_t:
            return left_t
        if isinstance(op, ast.Mult) and (
            (left_t in (str, bytes) and right_t is int)
            or (right_t in (str, bytes) and left_t is int)
        ):
            return left_t if left_t in (str, bytes) else right_t
        assert False, f"unsupported BinOp on {left_t} and {right_t}"

    def visit_BinOp(self, node: ast.BinOp):
        typ = self._binop_type(node.op, self.visit(node.left), self.visit(node.right))
        self.types[node] = typ
        return typ

    def visit_UnaryOp(self, node: ast.UnaryOp):
        operand_t = self.visit(node.operand)
        numeric = {bool, int, float, complex}

        match node.op:
            # not x  →  always bool, for any operand
            case ast.Not():
                typ = bool
            # +x / -x  →  numeric; bool collapses to int (-True == -1)
            case ast.UAdd() | ast.USub():
                assert operand_t in numeric, f"unary +/- on {operand_t}"
                typ = int if operand_t is bool else operand_t
            # ~x  →  integer bitwise invert; not valid on float/complex
            case ast.Invert():
                assert operand_t in (bool, int), f"unary ~ on {operand_t}"
                typ = int
            case _:
                assert False, f"unsupported UnaryOp {node.op}"

        self.types[node] = typ
        return typ

    def visit_AugAssign(self, node: ast.AugAssign):
        # Target must already be declared
        assert isinstance(node.target, ast.Name)
        name = node.target.id
        target_t = self.scope.lookup(name)
        assert target_t is not None, f"augmented assign to undeclared {name}"

        value_t = self.visit(node.value)
        result_t = self._binop_type(node.op, target_t, value_t)

        # static typing: the variable's type must not change
        if result_t != target_t:
            raise ValueError(
                f"{name} on line {node.lineno} is {target_t} but {name} {type(node.op).__name__} {value_t} is {result_t}"
            )
        assert (
            result_t == target_t
        ), f"{name} is {target_t} but {name} {type(node.op).__name__} {value_t} is {result_t}"

        self.types[node] = target_t
        return target_t

    def visit_If(self, node: ast.If):
        self.visit(node.test)
        for stmt in node.body:
            self.visit(stmt)
        for stmt in node.orelse:
            self.visit(stmt)
        return type(None)

    def visit_BoolOp(self, node: ast.BoolOp):
        # and / or return one of their operands, not necessarily bool:
        #   1 and 2  -> 2 (int);  "" or [] -> [] (list)
        # The result type is the union of the operand types. With no union
        # type yet, require them equal and return that type.
        operand_types = [self.visit(v) for v in node.values]
        assert all(
            t == operand_types[0] for t in operand_types
        ), f"mixed BoolOp operand types: {operand_types}"
        typ = operand_types[0]
        self.types[node] = typ
        return typ

    def visit_Compare(self, node: ast.Compare):
        # x < y, a == b == c, x in xs, x is None  →  always bool.
        # (Chained comparisons like a < b < c are still bool overall.)
        self.visit(node.left)
        for comparator in node.comparators:
            self.visit(comparator)
        typ = bool
        self.types[node] = typ
        return typ

    def visit_While(self, node: ast.While):
        self.visit(node.test)
        for stmt in node.body:
            self.visit(stmt)
        if node.orelse:
            self.visit(node.orelse)

    def visit_For(self, node: ast.For):
        self.visit(node.target)
        self.visit(node.iter)
        for stmt in node.body:
            self.visit(stmt)
        if node.orelse:
            self.visit(node.orelse)

    def visit_Continue(self, node: ast.Continue):
        return type(None)

    def visit_Break(self, node: ast.Break):
        return type(None)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.new_scope_type(ScopeType.CLASS)
        this_scope = self.scope
        # Get the type of the class member fields and functions
        members = []
        for stmt in node.body:
            members.append(self.visit(stmt))
        print(members)


class FunctionTypeInferrer(symbols.ScopingNodeVisitor):
    def visit_FunctionDef(self, node: ast.FunctionDef):
        args = node.args.args
        argument_types: list[type] = (
            []
        )  # Will be used later for the type of the function itself
        for arg in args:
            if not hasattr(arg, "annotation"):
                raise ValueError(
                    f"Parameter '{arg.arg}' for function '{node.name}' on line {node.lineno} does not have a type annotation"
                )
            typ = type_of_annotation(arg.annotation)
            argument_types.append(typ)
            function_scope.define(arg.arg, typ)
        if not hasattr(node, "returns"):
            raise ValueError(
                f"Function '{node.name}' on line {node.lineno} does not have a return type annotation"
            )
        return_type = type_of_annotation(node.returns)
        function_type = typing.Callable[argument_types, return_type]

        # Define the function in the outer scope and move to the function scope
        self.scope.define(node.name, function_type)
        self.scope = function_scope

        self.types[node] = function_type

        # if node.name != 'main': return
        for stmt in node.body:
            self.visit(stmt)

        self.scope = this_scope
        self.old_scope_type()


simple_annotation_type = {
    "int": int,
    "float": float,
    "bool": bool,
    "str": str,
    "list": list,
    "tuple": tuple,
    "set": set,
}


# Returns the python type that an annotation expresses
def type_of_annotation(annotation: ast.AST) -> type:
    match annotation:
        case ast.Name():
            return simple_annotation_type[annotation.id]
        case ast.Subscript():
            value_t = type_of_annotation(annotation.value)
            slice = annotation.slice
            if isinstance(slice, ast.Name):
                slice_t = type_of_annotation(slice)
                return value_t[slice_t]
            else:
                assert isinstance(slice, ast.Tuple)
                slice_types = [
                    type_of_annotation(element) for element in annotation.slice.elts
                ]
                return value_t[*slice_types]
