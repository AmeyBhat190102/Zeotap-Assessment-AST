import streamlit as st
import requests

# Define the base URL for your Flask API
API_URL = "http://127.0.0.1:5000"  # Flask running locally

st.title("Rule Engine Frontend")

# Input for rules
rule_input = st.text_area("Enter a single rule or multiple rules (comma-separated)", "")
is_multiple = st.checkbox("Multiple rules")

# Input for user data attributes
age = st.number_input("Age", min_value=0, max_value=100)
department = st.text_input("Department")
salary = st.number_input("Salary", min_value=0)
experience = st.number_input("Experience", min_value=0)

user_data = {
    "age": age,
    "department": department,
    "salary": salary,
    "experience": experience
}

if st.button("Submit Rule"):
    if is_multiple:
        # Handle multiple rules
        rule_list = rule_input.split(',')
        st.write(f"Entered Rule Strings :: {rule_list}")
        response = requests.post(f"{API_URL}/combine_rules", json={"rules": rule_list})
    else:
        # Handle single rule
        response = requests.post(f"{API_URL}/create_rule", json={"rule_string": rule_input})

    if response.status_code == 200:
        ast = response.json()['ast'] if 'ast' in response.json() else response.json()['combined_ast']
        st.write(f"Generated AST: {ast}")

        # Now evaluate the rule based on the provided data
        evaluate_response = requests.post(f"{API_URL}/evaluate_rule", json={"ast": ast, "data": user_data})

        if evaluate_response.status_code == 200:
            result = evaluate_response.json()["result"]
            st.write(f"Rule Evaluation Result: {result}")
        else:
            st.error("Error evaluating the rule.")
    else:
        st.error("Error creating the rule. ")

