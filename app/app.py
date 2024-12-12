from flask import Flask
from .database import init_db
from models.create_table import create_tables

def create_app():
    app = Flask(__name__)
    
    # Initialiser la base de données
    init_db(app)
    
    # Créer les tables nécessaires
    create_tables()
    
    # Enregistrer les blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app