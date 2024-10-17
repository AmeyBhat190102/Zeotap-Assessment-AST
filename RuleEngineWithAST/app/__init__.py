from flask import Flask
from .db import init_db

def create_app():
    app = Flask(__name__)
    init_db(app)
    from .api import api_blueprint
    app.register_blueprint(api_blueprint)
    return app
