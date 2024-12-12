from flask import Flask
from .database import init_db

def create_app():
    app = Flask(__name__)
    init_db(app)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app