USER_DEFINED_FUNCTIONS = {
    "is_senior": "is_senior"
}

def evaluate_rule(rule, data):
    def evaluate(node):
        if node.node_type == "function":
            func_name = node.value
            args = [evaluate(arg) for arg in node.args]  # Evaluate function arguments
            if func_name in USER_DEFINED_FUNCTIONS:
                return USER_DEFINED_FUNCTIONS[func_name](*args)
            else:
                raise ValueError(f"Function {func_name} not defined")
        elif node.node_type == "operand":
            return data[node.value.split()[0]]  # Assuming simple "attribute" access
        elif node.node_type == "operator":
            left_value = evaluate(node.left)
            right_value = evaluate(node.right)
            if node.value == "AND":
                return left_value and right_value
            elif node.value == "OR":
                return left_value or right_value

    return evaluate(rule)
