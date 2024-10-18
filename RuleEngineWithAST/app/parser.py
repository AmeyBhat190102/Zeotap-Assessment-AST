import ast
from .models import Node

def create_rule(rule_string):
    def parse_expression(expr):
        if isinstance(expr, ast.BoolOp):
            # Process all values in the BoolOp, not just the first two
            node = parse_expression(expr.values[0])
            for value in expr.values[1:]:
                if isinstance(expr.op, ast.And):
                    node = Node("operator", "AND", node, parse_expression(value))
                elif isinstance(expr.op, ast.Or):
                    node = Node("operator", "OR", node, parse_expression(value))
            return node
        elif isinstance(expr, ast.Compare):
            left = expr.left.id
            comparator = expr.ops[0]

            # Check if right-hand side is a number or a string
            if isinstance(expr.comparators[0], ast.Num):  # Handles numeric values
                right = expr.comparators[0].n
            elif isinstance(expr.comparators[0], ast.Str):  # Handles string values
                right = f"'{expr.comparators[0].s}'"
            else:
                raise ValueError("Unsupported comparator type")

            # Determine the operator type
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
