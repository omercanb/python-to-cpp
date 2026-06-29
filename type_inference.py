import ast
from dataclasses import dataclass, field
import types
from utils import dump

@dataclass
class Scope:
    # kind: str # "module" | "function" | "class"
    names: dict[str, type] = field(default_factory=dict)
    parent: "Scope | None" = None

    def lookup(self, name: str) -> type | None:
        scope = self
        while scope is not None:
            if name in scope.names:
                return scope.names[name]
            scope = scope.parent
        return None

    def define(self, name: str, t: type) -> None:
        self.names[name] = t


py_builtins = set(['print'])

# Used for empty containers like []
class Unkown: pass

# A basic type inference walker that will be changed later
# All the visit functions return python types
class TypeInferrer(ast.NodeVisitor):
    types: dict[ast.AST, type] = {}
    scope: Scope = Scope()
    def visit_Constant(self, node: ast.Constant):
        return type(node.value)

    # Returns a the type of the list element
    def visit_List(self, node: ast.List):
        # An empty list returns an unkown type which should be checked later
        if len(node.elts) == 0:
            return Unkown
        # Check that all elements of a list are of the same type
        assert all(self.visit(element) == self.visit(node.elts[0]) for element in node.elts)
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
            return Unkown

        # Name not in scope
        self.types[node] = Unkown
        # return Unkown
        raise ValueError(f'Variable {node.id} line {node.lineno} used without declaration')

    def visit_Assign(self, node: ast.Assign):
        assert len(node.targets) == 1
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
            raise ValueError(f'Annotated assignment {dump(node.target)} type {target_t} is different from assigned type {value_t}')
        return target_t

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name != 'main': return
        for stmt in node.body:
            self.visit(stmt)

    # Claude generated 
    def visit_BinOp(self, node: ast.BinOp):
        left_t = self.visit(node.left)
        right_t = self.visit(node.right)

        numeric_rank = {bool: 0, int: 1, float: 2, complex: 3}

        # True division always yields float (complex if either operand is complex)
        if isinstance(node.op, ast.Div) and left_t in numeric_rank and right_t in numeric_rank:
            typ = complex if complex in (left_t, right_t) else float

        # Other numeric arithmetic: promote to the wider type
        elif left_t in numeric_rank and right_t in numeric_rank:
            wider = left_t if numeric_rank[left_t] >= numeric_rank[right_t] else right_t
            # bool op bool yields int, not bool (True + True == 2)
            typ = int if wider is bool else wider

        # Concatenation of matching sequence/str types: str+str, list+list, etc.
        elif isinstance(node.op, ast.Add) and left_t == right_t:
            typ = left_t

        # Repetition: seq * int  or  int * seq
        elif isinstance(node.op, ast.Mult) and (
            (left_t in (str, bytes) and right_t is int) or
            (right_t in (str, bytes) and left_t is int)
        ):
            typ = left_t if left_t in (str, bytes) else right_t

        else:
            assert False, f'unsupported BinOp on {left_t} and {right_t}'

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
                assert operand_t in numeric, f'unary +/- on {operand_t}'
                typ = int if operand_t is bool else operand_t
            # ~x  →  integer bitwise invert; not valid on float/complex
            case ast.Invert():
                assert operand_t in (bool, int), f'unary ~ on {operand_t}'
                typ = int
            case _:
                assert False, f'unsupported UnaryOp {node.op}'

        self.types[node] = typ
        return typ


    def visit_BoolOp(self, node: ast.BoolOp):
        # and / or return one of their operands, not necessarily bool:
        #   1 and 2  -> 2 (int);  "" or [] -> [] (list)
        # The result type is the union of the operand types. With no union
        # type yet, require them equal and return that type.
        operand_types = [self.visit(v) for v in node.values]
        assert all(t == operand_types[0] for t in operand_types), \
            f'mixed BoolOp operand types: {operand_types}'
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



simple_annotation_type = {
    'int':   int,
    'float': float,
    'bool':  bool,
    'str':   str,
    'list': list,
    'tuple': tuple,
    'set': set,
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
                slice_types = [type_of_annotation(element) for element in annotation.slice.elts]
                return value_t[*slice_types]






