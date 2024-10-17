from RuleEngineWithAST.app.parser import create_rule
from RuleEngineWithAST.app.combiner import combine_rules
from RuleEngineWithAST.app.evaluator import evaluate_rule

def test_create_rule():
    rule_string = "age > 30 AND department = 'Sales'"
    ast_tree = create_rule(rule_string)
    assert ast_tree.node_type == "operator"

def test_combine_rules():
    rule1 = create_rule("age > 30 AND department = 'Sales'")
    rule2 = create_rule("salary > 50000 OR experience > 5")
    combined = combine_rules([rule1, rule2])
    assert combined.node_type == "operator"

def test_evaluate_rule():
    rule_string = "age > 30 AND department = 'Sales'"
    ast_tree = create_rule(rule_string)
    data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
    assert evaluate_rule(ast_tree, data) == True
