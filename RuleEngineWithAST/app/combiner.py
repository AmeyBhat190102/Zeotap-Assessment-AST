from .models import Node


def combine_rules(rules):
    if len(rules) == 1:
        return rules[0]

    combined_rule = rules[0]
    for rule in rules[1:]:
        combined_rule = Node("operator", "AND", combined_rule, rule)
    return combined_rule
