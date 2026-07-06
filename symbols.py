import ast
import builtins
from dataclasses import dataclass, field
from enum import Enum, auto
from pprint import pprint

from utils import dump


class ScopeType(Enum):
    BUILTIN = auto()
    MODULE = auto()
    FUNCTION = auto()
    CLASS = auto()
    COMPREHENSION = auto()


class SymbolType(Enum):
    # A variable that is not a class or instance variable
    VARIABLE = auto()
    # A class variable like A.x
    CLASS_VARIABLE = auto()
    # An instance variable like self.x = 10, where x is an instance variable
    INSTANCE_VARIABLE = auto()
    # A function not defined in a class
    FUNCTION = auto()
    # A function defined in a class taking a self parameter
    METHOD = auto()
    # The __init__ function defined in a class scope
    INIT = auto()
    # A function defined in a class with a @static_method decorator
    # STATIC_METHOD = auto()
    # A class
    CLASS = auto()


def print_indented(indent, *args, **kwargs):
    print(" " * indent, end="")
    print(*args, **kwargs)


def print_dict(d, indent):
    for k, v in d.items():
        print_indented(indent, f"{k}: {v}")


# The scope / scope tree responsible for maintaining definitions and resolutions
@dataclass
class Scope:
    typ: ScopeType
    name: str | None = None
    enclosing: "Scope | None" = None
    # Definitions contains both the symbol type and ast.stmt becase the ast.stmt can be useful and we can't recover the symbol type from the stmt in case of functions vs methods
    definitions: dict[str, tuple[SymbolType, ast.AST]] = field(default_factory=dict)
    children: list["Scope"] = field(default_factory=list)

    global_vars: set[str] = field(default_factory=set)
    nonlocal_vars: set[str] = field(default_factory=set)

    def define(self, name, symbol_type: SymbolType, stmt):
        assert name not in self.definitions
        self.definitions[name] = (symbol_type, stmt)

    def resolve(self, name, skip_class=False) -> tuple[SymbolType, ast.AST] | None:
        """
        Scope resolution rules for python
        If a the current scope is not a class scope, the symbol can't be resolved in a parent 'Class' scope
        The global qualifier affect resolution, but the nonlocal qualifier doesn't
        This happens in the case where a name is defined globally and in an enclosing scope, then the name should resolve to the gloval
        """
        skip = False
        if skip_class and self.typ == ScopeType.CLASS:
            skip = True

        if name in self.global_vars:
            return self.resolve_global_name(name)
        if name in self.definitions:
            return self.definitions[name]

        if not skip:
            if self.enclosing:
                return self.enclosing.resolve(name, skip_class=True)

        return None

    def resolve_global_name(self, name) -> tuple[SymbolType, ast.AST]:
        scope = self
        while scope.enclosing is not None:
            scope = scope.enclosing
        if name in scope.definitions:
            return scope.definitions[name]
        else:
            raise NameError("Global declared name not found in global namespace", name)

    def add_child(self, child_scope):
        self.children.append(child_scope)

    def add_global(self, name):
        self.global_vars.add(name)

    def add_nonlocal(self, name):
        self.nonlocal_vars.add(name)

    def print_tree(self, indent=0):
        print_indented(indent, self.typ, self.name)
        print_indented(indent, "definitions {")
        print_dict(self.definitions, indent)
        print_indented(indent, "}")
        if self.nonlocal_vars:
            print_indented(indent, f"nonlocals: {self.nonlocal_vars}")
        if self.global_vars:
            print_indented(indent, f"globals: {self.global_vars}")
        print_indented(indent, "child scopes {")
        for child in self.children:
            child.print_tree(indent + 4)
        print_indented(indent, "}")

    def print_self(self, indent=0):
        print_indented(indent, self.typ, self.name)
        print_indented(indent, "definitions {")
        print_dict(self.definitions, indent)
        if self.nonlocal_vars:
            print_indented(indent, f"nonlocals: {self.nonlocal_vars}")
        if self.global_vars:
            print_indented(indent, f"globals: {self.global_vars}")
        print_indented(indent, "}")


class ScopeTracker:
    def __init__(self, scope: Scope):
        self.scope = scope
        self.iter = iter(self)

    def __iter__(self):
        stack = [self.scope]
        while stack:
            cur = stack.pop()
            yield cur
            stack.extend(reversed(cur.children))

    def update(self, node: ast.AST):
        match node:
            case ast.ListComp() | ast.SetComp() | ast.DictComp() | ast.GeneratorExp():
                for _ in node.generators:
                    self.scope = next(self.iter)
            case ast.Module() | ast.FunctionDef() | ast.ClassDef():
                self.scope = next(self.iter)


# Visitor for the AST that keep track of the current scope
class ScopingNodeVisitor(ast.NodeVisitor):
    def __init__(self, scope: Scope):
        self.scope_tracker = ScopeTracker(scope)

    def scope(self):
        return self.scope_tracker.scope

    def visit(self, node: ast.AST):
        if node is None:
            return
        if isinstance(node, list):
            for child in node:
                self.visit(child)
        else:
            cur_scope = self.scope_tracker.scope
            self.scope_tracker.update(node)
            new_scope = self.scope_tracker.scope
            method = "visit_" + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)


# The first pass of scope resolution
# Creates a scope tree with all the definitions in every scope
@dataclass
class SymbolDefiner(ast.NodeVisitor):
    scope: Scope = field(default_factory=lambda: Scope(ScopeType.MODULE))

    def push_scope(self, scope_type: ScopeType, name=None):
        new_scope = Scope(scope_type, name, self.scope)
        self.scope.add_child(new_scope)
        self.scope = new_scope

    def pop_scope(self):
        assert self.scope.enclosing
        self.scope = self.scope.enclosing

    # implicit visit_Module

    def visit_many(self, nodes):
        for node in nodes:
            self.visit(node)

    def get_function_type(self, node: ast.FunctionDef):
        if self.scope.typ == ScopeType.CLASS:
            if node.name == "__init__":
                return SymbolType.INIT
            else:
                return SymbolType.METHOD
        else:
            return SymbolType.FUNCTION

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Define function in current scope and define parameters in the function scope
        symbol_type = self.get_function_type(node)
        self.scope.define(node.name, symbol_type, node)
        self.push_scope(ScopeType.FUNCTION, node.name)
        self.visit(node.args)
        if symbol_type == SymbolType.INIT:
            self.handle_init_def(node)
        self.visit_many(node.body)
        self.pop_scope()

    # Walk an initializer body to find all instances of self.x = Any and record x as an instance variable
    def handle_init_def(self, node: ast.FunctionDef):
        assert node.name == "__init__"
        assert self.scope.typ == ScopeType.FUNCTION
        self_param_name = node.args.args[0].arg
        for n in ast.walk(node):
            match n:
                # This case handles both assign and annotated assign because of ctx=Store()
                case ast.Attribute(
                    value=ast.Name(id=self_param_name, ctx=ast.Load()),
                    attr=instance_variable,
                    ctx=ast.Store(),
                ):
                    self.scope.define(
                        instance_variable, SymbolType.INSTANCE_VARIABLE, n
                    )
                    print("self assign", instance_variable, dump(n))

    def visit_ClassDef(self, node: ast.ClassDef):
        self.scope.define(node.name, SymbolType.CLASS, node)
        self.push_scope(ScopeType.CLASS, node.name)
        self.visit_many(node.body)
        self.pop_scope()

    def visit_arg(self, node: ast.arg):
        self.scope.define(node.arg, SymbolType.VARIABLE, node)

    def visit_Global(self, node: ast.Global):
        for name in node.names:
            self.scope.add_global(name)

    def visit_Nonlocal(self, node: ast.Nonlocal):
        for name in node.names:
            self.scope.add_nonlocal(name)

    # A definition can only happen on the lhs of assigns if there is a name with a store context
    def visit_Name(self, node: ast.Name):
        if not isinstance(node.ctx, ast.Store):
            return
        if self.scope.typ == ScopeType.CLASS:
            symbol_type = SymbolType.CLASS_VARIABLE
        else:
            symbol_type = SymbolType.VARIABLE
        name = node.id
        # Assignments to a nonlocal or global var are not definitions
        if name in self.scope.nonlocal_vars or name in self.scope.global_vars:
            return
        if name in self.scope.definitions:
            return
        self.scope.define(name, symbol_type, node)

    def visit_ListComp(self, node: ast.ListComp):
        self.handle_generators(node.generators)

    def visit_SetComp(self, node: ast.SetComp):
        self.handle_generators(node.generators)

    def visit_DictComp(self, node: ast.DictComp):
        self.handle_generators(node.generators)

    def visit_GeneratorExp(self, node: ast.GeneratorExp):
        self.handle_generators(node.generators)

    # Comprehensions create nested scopes but arent nested in the AST so we have to handle them manually
    def handle_generators(self, generators: list[ast.comprehension]):
        for generator in generators:
            self.push_scope(ScopeType.COMPREHENSION)
            match generator.target:
                case ast.Name(id=var, ctx=ast.Store()):
                    self.scope.define(var, SymbolType.VARIABLE, generator.target)
        for _ in generators:
            self.pop_scope()
