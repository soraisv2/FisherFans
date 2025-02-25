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

    # Enregistrement des blueprints
    from routes.users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    from routes.boats import boats as boat_blueprint
    app.register_blueprint(boat_blueprint)

    from routes.fishing_logs import fishing_logs_bp as fishing_logs_blueprint
    app.register_blueprint(fishing_logs_blueprint)
    
    from routes.fishing_trips import fishing_trips_bp as fishing_trips_blueprint
    app.register_blueprint(fishing_trips_blueprint)


    return app