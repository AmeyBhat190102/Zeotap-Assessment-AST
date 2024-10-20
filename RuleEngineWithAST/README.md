# Rule Engine 

This project is a Flask-based rule engine that allows users to create, combine, evaluate, and modify rules. The engine works by generating Abstract Syntax Trees (AST) from rule strings, validating attributes, handling errors, and supporting dynamic rule modifications. It also allows for custom functions in rules for advanced conditions.

## Features

- **Rule Creation**: Parse and create ASTs from rule strings.
- **Rule Combination**: Combine multiple ASTs into a single rule.
- **Rule Evaluation**: Evaluate rules based on provided data.
- **Error Handling**: Validation for incorrect rule strings, missing attributes, and invalid data formats.
- **Attribute Validation**: Ensure rule attributes are part of a pre-defined catalog.
- **Custom Functions**: Extend the rule engine with user-defined functions for advanced conditions.

## Endpoints

1. **`POST /create_rule`**: 
   - Converts a rule string into an AST.
   - Example Request:
     ```json
     {
       "rule_string": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
     }
     ```
   - Response:
     ```json
     {
       "ast": "AST_representation"
     }
     ```

2. **`POST /combine_rules`**:
   - Combines multiple rule strings into a single AST.
   - Example Request:
     ```json
     {
       "rules": ["rule1", "rule2"]
     }
     ```
   - Response:
     ```json
     {
       "combined_ast": "Combined_AST_representation"
     }
     ```

3. **`POST /evaluate_rule`**:
   - Evaluates a rule AST with given data.
   - Example Request:
     ```json
     {
       "ast": { "AST_representation" },
       "data": { "age": 35, "department": "Sales", "salary": 60000, "experience": 3 }
     }
     ```
   - Response:
     ```json
     {
       "result": true
     }
     ```

## Error Handling & Validation

- Invalid rule strings (e.g., missing operators or comparisons) will raise appropriate errors.
- Attributes in the rules are validated against a pre-defined set of valid attributes (e.g., `age`, `salary`, `department`).

## Setup Instructions

Follow these steps to set up the project locally:

### Prerequisites

- Python 3.x
- Flask
- Pip

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-repo-url/rule-engine.git
cd rule-engine
```

### Step 2: Create a Virtual Environment

Create a virtual environment to isolate dependencies.

```bash
python -m venv venv
source venv/bin/activate  # For Windows, use: venv\Scripts\activate
```

### Step 3: Install Dependencies

Install the required dependencies using `pip`.

```bash
pip install -r requirements.txt
```

### Step 4: Run the Flask App

Start the Flask server by running the following command:

```bash
python -m api.py
```

## Step 5: Test Endpoints

You can test the API endpoints using `Postman`, `curl`, or any other HTTP client.

### 1. Root Endpoint

To check if the server is running, use the following command:

```bash
curl http://127.0.0.1:5000/
```

```angular2html
Expected output message here 
{
  "message": "Server is running"
}
```

## Hitting the Create Rule Endpoint here 
```angular2html
Use the POST /create_rule endpoint to create an AST (Abstract Syntax Tree) from a rule string.

curl -X POST http://127.0.0.1:5000/create_rule -H "Content-Type: application/json" -d '{
  "rule_string": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
}'

Expected output format will be 

{
  "ast": "{\"type\": \"operator\", \"left\": {...}, \"right\": {...}, \"operator\": \"AND\"}"
}
```

## Hitting the Combine Rules Endpoints
```
Use the POST /combine_rules endpoint to combine two or more rules into a single AST.

curl -X POST http://127.0.0.1:5000/combine_rules -H "Content-Type: application/json" -d '{
  "rules": [
    "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)",
    "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
  ]
}'

Expected Output here will be

{
  "combined_ast": "{\"type\": \"operator\", \"left\": {...}, \"right\": {...}, \"operator\": \"AND\"}"
}
```

## Hitting the Evaluate Rule Endpoint
```angular2html
Use the POST /evaluate_rule endpoint to evaluate a rule using the AST and a data payload.

curl -X POST http://127.0.0.1:5000/evaluate_rule -H "Content-Type: application/json" -d '{
  "ast": {
    "type": "operator",
    "left": {
      "type": "operand",
      "value": "age"
    },
    "right": {
      "type": "operand",
      "value": 30
    },
    "operator": ">"
  },
  "data": {
    "age": 35,
    "department": "Sales",
    "salary": 60000,
    "experience": 3
  }
}'

Expected Output here 

{
  "result": true
}
```