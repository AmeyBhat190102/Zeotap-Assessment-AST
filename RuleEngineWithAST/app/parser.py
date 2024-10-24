import ast
from .models import Node

VALID_ATTRIBUTES = {"age", "salary", "department", "experience"}
USER_DEFINED_FUNCTIONS = {"is_senior"}

def validate_rule(rule):
    if rule.node_type == "operand":
        attribute = rule.value.split()[0]
        if attribute not in VALID_ATTRIBUTES:
            raise ValueError(f"Invalid attribute: {attribute}")
    elif rule.node_type == "function":
        if rule.value not in USER_DEFINED_FUNCTIONS:
            raise ValueError(f"Function {rule.value} is not defined.")
        # Validate function arguments
        for arg in rule.args:
            validate_rule(arg)  # Recursively validate function arguments
    elif rule.node_type == "operator":
        validate_rule(rule.left)
        validate_rule(rule.right)

def create_rule(rule_string):
    def parse_expression(expr):
        if isinstance(expr, ast.Call):  # Function call like is_senior(age)
            func_name = expr.func.id
            args = [parse_expression(arg) for arg in expr.args]  # Parse function arguments
            return Node("function", func_name, args=args)
        elif isinstance(expr, ast.BoolOp):
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
            if isinstance(expr.comparators[0], ast.Num):
                right = expr.comparators[0].n
            elif isinstance(expr.comparators[0], ast.Str):
                right = f"'{expr.comparators[0].s}'"
            else:
                raise ValueError("Unsupported comparator type")

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
    ast_tree = parse_expression(expr_tree.body)

    # Validate the AST for attributes and functions
    validate_rule(ast_tree)
    return ast_tree
