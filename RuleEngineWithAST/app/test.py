import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# Test the root endpoint
def test_root():
    response = requests.get(f"{BASE_URL}/")
    print("Root Endpoint Response:", response.json())

# Test the create_rule endpoint
def test_create_rule():
    payload = {
        "rule_string": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    }
    response = requests.post(f"{BASE_URL}/create_rule", json=payload)
    print("Create Rule Response:", response.json())

# Test the combine_rules endpoint
def test_combine_rules():
    payload = {
        "rules": [
            "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)",
            "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
        ]
    }
    response = requests.post(f"{BASE_URL}/combine_rules", json=payload)
    print("Create Rule Response:", response.json())

# Test the evaluate_rule endpoint
def test_evaluate_rule():
    payload = {
        "ast": {
            "node_type": "operand",
            "value" : "age > 30"
        },
        "data": {
            "age": 35,
            "department": "Sales",
            "salary": 60000,
            "experience": 3
        }
    }
    response = requests.post(f"{BASE_URL}/evaluate_rule", json=payload)
    print("Evaluate Rule Response:", response.text)

if __name__ == "__main__":
    # Test all endpoints
    test_root()
    test_create_rule()
    test_combine_rules()
    test_evaluate_rule()
