import ast, math

locals = {key: value for (key, value) in vars(math).items() if key[0] != '_'}
locals.update({"abs": abs, "complex": complex, "min": min, "max": max, "pow": pow, "round": round})


class Formula:
    def __init__(self, expr):
        self.expr = expr
        if any(elem in self.expr for elem in '\n#'): raise ValueError(expr)
        try:
            node = ast.parse(self.expr.strip(), mode='eval')
            self.Visitor().visit(node)
            self.compiled_expr = compile(node, "<string>", "eval")
            self.variables = self.compiled_expr.co_names
            self.constants = self.compiled_expr.co_consts
        except Exception:
            raise ValueError(self.expr)

    class Visitor(ast.NodeVisitor):
        def visit(self, node):
            if not isinstance(node, self.whitelist):
                raise ValueError(node)
            return super().visit(node)

        whitelist = (ast.Module, ast.Expr, ast.Load, ast.Expression, ast.Add, ast.Sub, ast.UnaryOp, ast.Num, ast.BinOp,
                     ast.Mult, ast.Div, ast.Pow, ast.BitOr, ast.BitAnd, ast.BitXor, ast.USub, ast.UAdd, ast.FloorDiv,
                     ast.Mod,
                     ast.LShift, ast.RShift, ast.Invert, ast.Call, ast.Name)

    def evaluate(self, locals={}):
        try:
            return eval(self.compiled_expr, {'__builtins__': None}, locals)
        except Exception as e:
            raise ValueError(f'{self.expr}: {str(e)}')
