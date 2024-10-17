import ast
from .models import Node

def create_rule(rule_string):
    def parse_expression(expr):
        if isinstance(expr, ast.BoolOp):
            if isinstance(expr.op, ast.And):
                return Node("operator", "AND", parse_expression(expr.values[0]), parse_expression(expr.values[1]))
            elif isinstance(expr.op, ast.Or):
                return Node("operator", "OR", parse_expression(expr.values[0]), parse_expression(expr.values[1]))
        elif isinstance(expr, ast.Compare):
            left = expr.left.id
            comparator = expr.ops[0]
            right = expr.comparators[0].n
            op = ">"
            if isinstance(comparator, ast.Gt):
                op = ">"
            elif isinstance(comparator, ast.Lt):
                op = "<"
            elif isinstance(comparator, ast.Eq):
                op = "="
            return Node("operand", f"{left} {op} {right}")
        else:
            raise ValueError("Unsupported expression")

    expr_tree = ast.parse(rule_string, mode='eval')
    return parse_expression(expr_tree.body)
