from flask import Flask, Blueprint, request, jsonify
from .parser import create_rule
from .combiner import combine_rules
from .evaluator import evaluate_rule
from .models import Node
import json

# Initialize Flask app
app = Flask(__name__)

# Define the API blueprint
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/create_rule', methods=['POST'])
def create_rule_api():
    rule_string = request.json['rule_string']
    rule_string = rule_string.strip()  # Removes unwanted spaces or newlines
    rule_string = rule_string.replace("AND", "and").replace("OR", "or").replace("NOT", "not").replace("=", "==")
    print("Rule String is : ", rule_string)
    ast_tree = create_rule(rule_string)
    return jsonify({"ast": json.dumps(ast_tree.to_dict())})  # Convert to dict here

@api_blueprint.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    rule_strings = request.json['rules']
    print("Rule Strings is : ", rule_strings)

    rules = []
    for rule in rule_strings:
        rule = rule.strip()  # Removes unwanted spaces or newlines
        rule = rule.replace("AND", "and").replace("OR", "or").replace("NOT", "not").replace("=", "==")
        rules.append(create_rule(rule))
    combined_ast = combine_rules(rules)
    return jsonify({"combined_ast": json.dumps(combined_ast.to_dict())})

@api_blueprint.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    ast_json = request.json['ast']
    data = request.json['data']

    # If ast_json is a string, parse it to a dictionary
    if isinstance(ast_json, str):
        ast_json = json.loads(ast_json)

    ast_tree = Node(**ast_json)
    print("AST Tree is : ", ast_tree)
    result = evaluate_rule(ast_tree, data)
    print("Result is : ", result)
    return jsonify({"result": result})

# Root endpoint to check server status
@app.route('/', methods=['GET'])
def root():
    return jsonify({"message": "Server is running"}), 200

# Register the blueprint with the app
app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    print("Starting the server...")
    app.run(debug=True)
