import ast
import scope
from utils import dump, build_and_run

ANNOTATION_TYPES = {
    "int":   int,
    "float": float,
    "bool":  bool,
    "str":   str,
}

def main():
    file = "input.py"
    tree = ast.parse(open(file).read())

    infer_types(tree)
    print(dump(tree, indent=4))

    scope.ScopeResolver().visit(tree)

    translated = CppTranslator().visit(tree)
    build_and_run(translated)


def infer_types(tree: ast.AST):
    for node in ast.walk(tree):
        match node:
            case ast.AnnAssign(target=ast.Name(), annotation=ast.Name()):
                node.target.inferred_type = ANNOTATION_TYPES.get(node.annotation.id)


class CppTranslator(ast.NodeVisitor):
    def visit_Module(self, node: ast.Module):
        s = '#include <iostream>'
        s += '\n\n'
        s += '\n\n'.join(self.visit(child) or '' for child in node.body)
        return s

    def visit_Expr(self, node: ast.Expr):
        return f'{self.visit(node.value)};'

    def visit_Call(self, node: ast.Call):
        # TODO change this to add an explicit print function and use it
        if isinstance(node.func, ast.Name) and node.func.id == 'print':
            if not node.args:
                return f'std::cout << "\\n"'
            args = ' << " " << '.join(self.visit(arg) or "" for arg in node.args)
            return f'std::cout << {args} << "\\n"'
        else:
            s = f'{self.visit(node.func)}('
            s += ', '.join(self.visit(arg) for arg in node.args)
            s += ')'
            return s
        

    def visit_AnnAssign(self, node: ast.AnnAssign):
        # What happens if nested assigns happen
        assert(isinstance(node.target, ast.Name))
        assert(hasattr(node.target, 'inferred_type'))
        assert(hasattr(node.target, 'is_declaration'))
        if node.target.is_declaration:
            if node.value:
                return f"{cpp_type(node.target.inferred_type)} {node.target.id} = {self.visit(node.value)};"
            else:
                return f"{cpp_type(node.target.inferred_type)} {node.target.id};"
        else:
            if node.value:
                return f"{node.target.id} = {self.visit(node.value)};"
            else:
                return f"{node.target.id};"

    def visit_Assign(self, node: ast.Assign):
        s = ''
        for target in node.targets:
            assert(isinstance(target, ast.Name))
        s += ' = '.join(target.id for target in node.targets)
        if node.value:
            s += f' = {self.visit(node.value)};'
        else:
            s += ';'
        return s

    def visit_AugAssign(self, node: ast.AugAssign):
        return f'{self.visit(node.target)} {cpp_op(node.op)}= {self.visit(node.value)};'

    def visit_Constant(self, node: ast.Constant):
        return f"{node.value}"

    def visit_BinOp(self, node: ast.BinOp):
        return f"({self.visit(node.left)} {cpp_op(node.op)} {self.visit(node.right)})"

    def visit_Name(self, node: ast.Name):
        return f"{node.id}"

    def visit_If(self, node: ast.If):
        s = ''
        # Hack to make it so we don't parenthesize the bool op twice
        if isinstance(node.test, ast.BoolOp):
            s += f'if {self.visit(node.test)} {{\n'
        else:
            s += f'if ({self.visit(node.test)}) {{\n'
        for stmt in node.body:
            s += f'{self.visit(stmt)}\n'
        if node.orelse:
            s += '} else {\n'
            for stmt in node.orelse:
                s += f'{self.visit(stmt)}\n'
        s += '}\n'
        return s

    def visit_IfExp(self, node: ast.IfExp):
        # Need to parenthesize because precedence of ternary is low in c++
        return f'({self.visit(node.test)} ? {self.visit(node.body)} : {self.visit(node.orelse)})'

    # Currently this is not quite right because an if(x) in python will use a truthiness condition while in c++ it may be different
    # For when we have only number types though, this is fine
    def visit_BoolOp(self, node: ast.BoolOp):
        s = '('
        s += f' {cpp_op(node.op)} '.join(self.visit(expr) for expr in node.values)
        s += ')'
        return s

    def visit_Compare(self, node: ast.Compare):
        # In python comparisons can be chained like a <= b < c
        # We need to convert that to (a <= b) && (b <= c)
        assert len(node.ops) >= 1
        assert len(node.ops) == len(node.comparators)
        for op in node.ops:
            assert is_cpp_op(op)
        # If there is just one comparison we don't need to parenthesize
        if len(node.ops) == 1:
            s = f'{self.visit(node.left)} {cpp_op(node.ops[0])} {self.visit(node.comparators[0])}'
        else:
            s = f'({self.visit(node.left)} {cpp_op(node.ops[0])} {self.visit(node.comparators[0])})'
            for i in range(1, len(node.ops)):
                s += f' && ({self.visit(node.comparators[i-1])} {cpp_op(node.ops[i])} {self.visit(node.comparators[i])})'
        return s

    def visit_FunctionDef(self, node: ast.FunctionDef):
        s = ''
        if node.name == 'main':
            s += f'int main('
        else:
            assert node.returns
            if isinstance(node.returns, ast.Constant):
                assert node.returns.value == None
                return_type = 'void'
            else:
                assert isinstance(node.returns, ast.Name)
                assert node.returns.id in ANNOTATION_TYPES 
                return_type = cpp_type(ANNOTATION_TYPES[node.returns.id])
            s += f'{return_type} {node.name}('
        s += ', '.join(f'{cpp_type(ANNOTATION_TYPES[arg.annotation.id])} {arg.arg}' for arg in node.args.args)
        s += ') {\n'
        for stmt in node.body:
            s += f'{self.visit(stmt)}\n'
        s += '}\n\n '
        return s

    def visit_Return(self, node: ast.Return):
        if node.value:
            return f'return {self.visit(node.value)};'
        else:
            return f'return;'

# Python type  ->  C++ type
CPP_TYPES = {
    int:   "int",
    float: "double",
    bool:  "bool",
    str:   "std::string",
    type(None): "void",
}

def cpp_type(t):
    try:
        return CPP_TYPES[t]
    except KeyError:
        raise NotImplementedError(f"no C++ mapping for {t.__name__}")

# AST operator class  ->  C++ symbol
CPP_OPS = {
    # arithmetic (ast.BinOp)
    ast.Add:  "+",
    ast.Sub:  "-",
    ast.Mult: "*",
    ast.Div:  "/",          # NOTE: semantics differ
    ast.Mod:  "%",
    ast.LShift: "<<",
    ast.RShift: ">>",
    ast.BitOr:  "|",
    ast.BitXor: "^",
    ast.BitAnd: "&",
    # comparison (ast.Compare)
    ast.Eq:  "==",
    ast.NotEq: "!=",
    ast.Lt:  "<",
    ast.LtE: "<=",
    ast.Gt:  ">",
    ast.GtE: ">=",
    # boolean (ast.BoolOp)
    ast.And: "&&",
    ast.Or:  "||",
    # unary (ast.UnaryOp)
    ast.UAdd: "+",
    ast.USub: "-",
    ast.Not:  "!",
    ast.Invert: "~",
}

def cpp_op(op):
    try:
        return CPP_OPS[type(op)]
    except KeyError:
        raise NotImplementedError(f"no C++ mapping for {type(op).__name__}")

def is_cpp_op(op):
    return type(op) in CPP_OPS

main()
