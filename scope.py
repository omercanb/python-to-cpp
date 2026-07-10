from __future__ import annotations

import ast
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from pprint import pp
from typing import TYPE_CHECKING

from tabulate import tabulate

if TYPE_CHECKING:
    from symbol_declaration import SymbolType

#
# class ScopeResolver(ast.NodeVisitor):
#     def __init__(self):
#         self.scope = Scope(ScopeType.MODULE)
#
#     def visit_FunctionDef(self, node: ast.FunctionDef):
#         # Inside a function, create a new scope
#         self.scope = Scope(node.name, self.scope)
#         self.generic_visit(node)
#         self.scope = self.scope.enclosing
#
#     def visit_AnnAssign(self, node: ast.AnnAssign):
#         # Continue with defining assign target and resolving from here
#         # Also handle for attribute and subscript
#         # if isinstance(node.target, ast.Name):
#         #     target = node.target.id
#         # # Think back on how to handle attributes as targets
#         # elif isinstance(node.target, ast.Attribute):
#         #     target = node.target.value
#         # else:
#         #     assert False
#         if isinstance(node.target, ast.Name):
#             if self.scope.resolve(node.target.id):
#                 node.target.is_declaration = False
#             else:
#                 node.target.is_declaration = True
#                 self.scope.define(node.target.id)
#         self.generic_visit(node)
#
#     def visit_Assign(self, node: ast.Assign):
#         assert len(node.targets) == 1
#         target = node.targets[0]
#         if isinstance(target, ast.Name):
#             if self.scope.resolve(target.id):
#                 target.is_declaration = False
#             else:
#                 target.is_declaration = True
#                 self.scope.define(target.id)
#         self.generic_visit(node)


class ScopeType(Enum):
    BUILTIN = auto()
    MODULE = auto()
    FUNCTION = auto()
    CLASS = auto()
    COMPREHENSION = auto()


def print_indented(indent, *args, **kwargs):
    print(" " * indent, end="")
    print(*args, **kwargs)


def print_dict(d, indent):
    for k, v in d.items():
        print_indented(indent, f"{k}: {v}")


@dataclass(eq=False)
class Scope:
    """
    The scope / scope tree responsible for maintaining definitions and resolutions
    """

    typ: ScopeType
    name: str | None = None
    enclosing: "Scope | None" = None
    # Definitions contains both the symbol type and ast.stmt becase the ast.stmt can be useful and we can't recover the symbol type from the stmt in case of functions vs methods
    definitions: dict[str, tuple[SymbolType, ast.AST]] = field(default_factory=dict)
    children: list["Scope"] = field(default_factory=list)

    global_vars: set[str] = field(default_factory=set)
    nonlocal_vars: set[str] = field(default_factory=set)

    def declare(self, name, symbol_type: SymbolType, stmt):
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


@dataclass
class ScopeTreeCreator(ast.NodeVisitor):
    scope: Scope = field(default_factory=lambda: Scope(ScopeType.MODULE))
    node_scopes: dict[ast.AST, Scope] = field(default_factory=dict)

    def visit(self, node: ast.AST | list):
        if node is None:
            return
        if isinstance(node, list):
            for child in node:
                self.visit(child)
        else:
            self.node_scopes[node] = self.scope
            method = "visit_" + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)

    def push_scope(self, scope_type: ScopeType, name=None):
        new_scope = Scope(scope_type, name, self.scope)
        self.scope.add_child(new_scope)
        self.scope = new_scope

    def pop_scope(self):
        assert self.scope.enclosing
        self.scope = self.scope.enclosing

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Visit decorators and annotations in enclosing scope
        self.push_scope(ScopeType.FUNCTION, node.name)
        self.visit(node.decorator_list)
        self.visit(node.args)
        if node.returns:
            self.visit(node.returns)
        # Visit body in function scope
        self.visit(node.body)
        self.pop_scope()

    def visit_ClassDef(self, node: ast.ClassDef):
        # Visit decorators, bases, and keywords in enclosing scope
        self.visit(node.decorator_list)
        self.visit(node.bases)
        self.visit(node.keywords)
        # Visit body in class scope
        self.push_scope(ScopeType.CLASS, node.name)
        self.visit(node.body)
        self.pop_scope()

    def visit_ListComp(self, node: ast.ListComp):
        self.handle_generators([node.elt], node.generators)

    def visit_SetComp(self, node: ast.SetComp):
        self.handle_generators([node.elt], node.generators)

    def visit_DictComp(self, node: ast.DictComp):
        self.handle_generators([node.key, node.value], node.generators)

    def visit_GeneratorExp(self, node: ast.GeneratorExp):
        self.handle_generators([node.elt], node.generators)

    # Comprehensions create nested scopes but arent nested in the AST so we have to handle them manually
    def handle_generators(
        self, elements: list[ast.AST], generators: list[ast.comprehension]
    ):
        first_generator, *other_generators = generators
        # The first iterator needs to be evaluated in the enclosing scope
        self.visit(first_generator.iter)
        # Only one scope is created regardless of the number of generators
        self.push_scope(ScopeType.COMPREHENSION)
        self.visit(first_generator.target)
        self.visit(first_generator.ifs)
        self.visit(elements)
        self.visit(other_generators)
        self.pop_scope()


class ScopeTracker:
    def __init__(self, node_scopes: dict[ast.AST, Scope]):
        self.node_scopes = node_scopes
        self.scope = next(iter(node_scopes.values()))

    def __iter__(self):
        stack = [self.scope]
        while stack:
            cur = stack.pop()
            yield cur
            stack.extend(reversed(cur.children))

    def update(self, node: ast.AST):
        if node in self.node_scopes:
            self.scope = self.node_scopes[node]


class ScopingNodeVisitor(ast.NodeVisitor):
    """
    Visitor for the AST that keep track of the current scope
    """

    def __init__(self, node_scopes):
        self.scope_tracker = ScopeTracker(node_scopes)

    def scope(self):
        return self.scope_tracker.scope

    def node_scopes(self):
        return self.scope_tracker.node_scopes

    def visit(self, node: ast.AST | list):
        if node is None:
            return
        if isinstance(node, list):
            for child in node:
                self.visit(child)
        else:
            self.scope_tracker.update(node)
            method = "visit_" + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)
