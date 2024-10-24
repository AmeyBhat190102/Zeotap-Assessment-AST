import streamlit as st
import requests
import json

# Define the base URL for your Flask API
API_URL = "http://127.0.0.1:5000"  # Flask running locally

st.title("Rule Engine Frontend")

# Create pages with a sidebar
page = st.sidebar.selectbox("Choose a page", ["Create Rule", "View/Edit Rules"])

# Page 1: Create Rule
if page == "Create Rule":
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

                # Store the rule and result in the database
                rule_data = {
                    "rule_string": rule_input,
                    "user_data": json.dumps(user_data),  # Convert user_data to a JSON string for DB storage
                    "result": result
                }
                insert_response = requests.post(f"{API_URL}/insert_rule", json=rule_data)

                if insert_response.status_code == 200:
                    st.success("Rule and result stored in the database.")
                else:
                    st.error("Failed to store rule and result in the database.")
            else:
                st.error("Error evaluating the rule.")
        else:
            st.error("Error creating the rule.")

# Page 2: View/Edit Rules
elif page == "View/Edit Rules":
    st.header("View or Edit Existing Rules")

    # Fetch all available rules from the DB (GET request to Flask API)
    rule_id = st.number_input("Enter Rule ID to Fetch", min_value=1)

    if st.button("Fetch Rule"):
        response = requests.get(f"{API_URL}/get_rule/{rule_id}")

        if response.status_code == 200:
            rule_data = response.json()

            # Display current rule data
            st.write(f"Rule ID: {rule_data['rule_id']}")
            rule_string = st.text_area("Rule String", value=rule_data['rule_string'])
            user_data_json = rule_data['user_data']
            result = rule_data['result']

            # Parse user_data from JSON string to dictionary
            user_data = json.loads(user_data_json)
            age = st.number_input("Age", value=user_data["age"])
            department = st.text_input("Department", value=user_data["department"])
            salary = st.number_input("Salary", value=user_data["salary"])
            experience = st.number_input("Experience", value=user_data["experience"])

            # If the "Update Rule" button is clicked, update the rule in the database
            if st.button("Update Rule"):
                updated_user_data = {
                    "age": age,
                    "department": department,
                    "salary": salary,
                    "experience": experience
                }

                # Re-evaluate the rule with updated data
                evaluate_response = requests.post(f"{API_URL}/evaluate_rule", json={
                    "ast": rule_data['rule_string'],
                    "data": updated_user_data
                })

                if evaluate_response.status_code == 200:
                    updated_result = evaluate_response.json().get("result")

                    # Send updated rule, user data, and result to Flask API to update in the DB
                    update_response = requests.post(f"{API_URL}/update_rule/{rule_id}", json={
                        "rule_string": rule_string,
                        "user_data": updated_user_data,
                        "result": updated_result
                    })

                    if update_response.status_code == 200:
                        st.success(f"Rule {rule_id} updated successfully.")
                    else:
                        st.error("Failed to update the rule.")
                else:
                    st.error("Error evaluating the updated rule.")
        else:
            st.error("Failed to fetch rule from the database.")
