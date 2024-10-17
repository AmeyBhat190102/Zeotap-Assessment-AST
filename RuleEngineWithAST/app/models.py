class Node:
    def __init__(self, node_type=None, value=None, left=None, right=None, **kwargs):
        self.node_type = node_type  # "operator" for AND/OR, "operand" for conditions
        self.value = value          # Used for operand nodes (age > 30)
        self.left = left            # Left child for operators
        self.right = right          # Right child for operators

    def to_dict(self):
        return {
            "node_type": self.node_type,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }