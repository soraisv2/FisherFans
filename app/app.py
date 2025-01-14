from flask import Flask, flash
import secrets
from .database import init_db
from models.create_table import create_tables

def create_app():
    app = Flask(__name__)
    
    # Securise session
    secret_key = secrets.token_hex(24)
    app.secret_key = secret_key
    
    # Initialiser la base de données
    init_db(app)
    
    # Créer les tables nécessaires
    create_tables()
    
    # Enregistrer les blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app