import psycopg2
from flask import g

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            database="zeotap_ast",
            user="root",
            password="amey",
            host="localhost"
        )
    return g.db

def init_db(app):
    @app.teardown_appcontext
    def close_db(error):
        db = g.pop('db', None)
        if db is not None:
            db.close()
