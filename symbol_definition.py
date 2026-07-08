from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING

from py_types import ClassType, FunctionType
from scope import ScopeType, ScopingNodeVisitor

if TYPE_CHECKING:
    from py_types import PyType
    from scope import Scope


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


# Creates a scope tree with all the definitions in every scope
class SymbolDefiner(ScopingNodeVisitor):
    """
    Define variables, functions, and classes
    Create stub types for functions and classes
    """

    def __init__(self, node_scopes):
        super().__init__(node_scopes)
        self.declared_types: dict[ast.AST, FunctionType | ClassType] = {}

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # If the node is a method, we don't wan't to define it as we'll do it when add a type to the class
        if self.scope().typ != ScopeType.CLASS:
            # Define function in current scope and define parameters in the function scope
            self.scope().define(node.name, SymbolType.FUNCTION, node)
            self.declared_types[node] = FunctionType(node)
        self.visit(node.args)
        self.visit(node.body)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.scope().define(node.name, SymbolType.CLASS, node)
        self.declared_types[node] = ClassType(node)
        self.visit(node.body)

    def visit_arg(self, node: ast.arg):
        self.scope().define(node.arg, SymbolType.VARIABLE, node)

    def visit_Global(self, node: ast.Global):
        for name in node.names:
            self.scope().add_global(name)

    def visit_Nonlocal(self, node: ast.Nonlocal):
        for name in node.names:
            self.scope().add_nonlocal(name)

    # A definition can only happen on the lhs of assigns if there is a name with a store context
    def visit_Name(self, node: ast.Name):
        if not isinstance(node.ctx, ast.Store):
            return
        name = node.id
        # Assignments to a nonlocal or global var are not definitions
        if name in self.scope().nonlocal_vars or name in self.scope().global_vars:
            return
        if name in self.scope().definitions:
            return
        self.scope().define(name, SymbolType.VARIABLE, node)
