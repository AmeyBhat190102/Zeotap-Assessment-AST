import psycopg2
from flask import g

# Establish the database connection
def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            database="zeotap_ast",
            user="root",
            password="amey",
            host="localhost"
        )
    return g.db

# Close the database connection
def init_db(app):
    @app.teardown_appcontext
    def close_db(error):
        db = g.pop('db', None)
        if db is not None:
            db.close()

# Create the rules table if it doesn't already exist
def create_rules_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id SERIAL PRIMARY KEY,
            rule_string TEXT NOT NULL,
            user_data JSON NOT NULL,
            result TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
    ''')
    db.commit()
    cursor.close()

# Insert a new rule, user data, and result into the database
def insert_rule(rule_string, user_data, result):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO rules (rule_string, user_data, result) VALUES (%s, %s, %s)',
                   (rule_string, user_data, result))
    db.commit()
    cursor.close()

# Update an existing rule in the database by rule ID
def update_rule(rule_id, rule_string, user_data, result):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE rules SET rule_string = %s, user_data = %s, result = %s, updated_at = NOW() WHERE id = %s',
                   (rule_string, user_data, result, rule_id))
    db.commit()
    cursor.close()

# Retrieve a rule by its ID from the database
def get_rule_by_id(rule_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM rules WHERE id = %s', (rule_id,))
    rule = cursor.fetchone()
    cursor.close()
    return rule
