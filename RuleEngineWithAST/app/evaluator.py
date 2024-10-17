def evaluate_rule(rule, data):
    def evaluate(node):
        print("Node type is : ",node.node_type)
        if node.node_type == "operand":
            key, op, value = node.value.split()
            value = int(value)
            if op == ">":
                return data[key] > value
            elif op == "<":
                return data[key] < value
            elif op == "=":
                return data[key] == value
        elif node.node_type == "operator":
            if node.value == "AND":
                return evaluate(node.left) and evaluate(node.right)
            elif node.value == "OR":
                return evaluate(node.left) or evaluate(node.right)

    return evaluate(rule)
