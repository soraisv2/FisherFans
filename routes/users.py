from flask import Blueprint, request, jsonify, session, redirect, url_for, current_app
from app.database import get_db
from models.users import get_users, add_user, get_user, delete_user, modify_user, login_user
from models.boats import get_user_boats
from models.fishing_logs import get_user_fishing_log
from models.fishing_trips import get_user_trips
from models.reservation import get_user_reservations
# JWT secure import
import jwt, datetime
from app.utils import token_required

users = Blueprint('users', __name__)

@users.route('/v1/users', methods=['POST'])
def user_actions():
    data = request.get_json()

    if not data or "action" not in data:
        return jsonify({"message": "Missing 'action' field in request. 🛑"}), 400

    action = data["action"]

    if action == "register":
        required_fields = [
            "action", "last_name", "first_name", "email", "password", "boat_license_number", 
            "date_of_birth", "phone", "address", "postal_code", "city", 
            "spoken_languages", "avatar_url", "insurance_number"
        ]
        
        if not all(k in data for k in required_fields):
            return jsonify({"message": "Missing registration fields. 🛑"}), 400

        success, message = add_user(
            data["last_name"], data["first_name"], data["email"], data["password"], 
            data["boat_license_number"], data["date_of_birth"], data["phone"],
            data["address"], data["postal_code"], data["city"], 
            data["spoken_languages"], data["avatar_url"], data["insurance_number"]
        )
        status_code = 201 if success else 409  # 201 = Created, 409 = Conflict (email déjà utilisé)
        return jsonify({"message": message}), status_code

    elif action == "login":
        if not all(k in data for k in ["email", "password"]):
            return jsonify({"message": "Missing login fields. 🛑"}), 400

        success, user = login_user(data["email"], data["password"])
        if success:
            token = jwt.encode(
                {
                    "user_id": user[0],  
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                },
                current_app.config["SECRET_KEY"],
                algorithm="HS256"
            )
            return jsonify({"message": "User successfully connected ✅", "token": token}), 200
        else:
            return jsonify({"message": "Incorrect email or password. 🛑"}), 404

    else:
        return jsonify({"message": "Invalid action. Use 'register' or 'login'. 🛑"}), 400


@users.route('/v1/users/<int:user_id>', methods=['GET'])
@token_required
def get_user_by_id(user_id):
    # Récupérer les données de l'utilisateur
    user = get_user(user_id)
    if user:
        # Récupérer les listes associées
        boats = get_user_boats(user_id)  # Récupère la liste des bateaux
        fishing_log = get_user_fishing_log(user_id)  # Récupère le journal de pêche
        trips = get_user_trips(user_id)  # Récupère les voyages de pêche
        reservations = get_user_reservations(user_id)  # Récupère les réservations

        # Construire le dictionnaire de l'utilisateur
        user_dict = {
            "id": user[0],
            "nom": user[1],
            "prenom": user[2],
            "email": user[3],
            "mot_de_passe": user[4],
            "boats": boats,  # Ajouter les bateaux
            "fishing_log": fishing_log,  # Ajouter le journal de pêche
            "trips": trips,  # Ajouter les voyages
            "reservations": reservations  # Ajouter les réservations
        }
        return jsonify(user_dict), 200
    else:
        return jsonify({"message": "Error while retrieving user. 🛑"}), 404


@users.route('/v1/users', methods=['GET'])
@token_required
def get_all_users():
    success, users = get_users()
    if success:
        user_list = [
            {
                "id": user[0],
                "nom": user[1],
                "prenom": user[2],
                "email": user[3],
                "mot_de_passe": user[4]
            }
            for user in users
        ]
        return jsonify(user_list)
    else:
        return jsonify({"message": "Error while retrieving users. 🛑"}), 404



@users.route('/v1/users/<int:user_id>', methods=['PUT'])
@token_required
def modify_user_route(user_id):
    data = request.get_json()

    # Vérifier que tous les champs requis sont présents et non vides
    required_fields = ["lastName", "firstName", "email", "boat_license_number"]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"message": "Tous les champs doivent être remplis. 🛑"}), 400  # 400 = Bad Request

    user = get_user(user_id)
    if user:
        modify_user(user_id, data["lastName"], data["firstName"], data["email"], data["boat_license_number"])
        return jsonify({"message": f"Utilisateur avec l'id {user_id} modifié avec succès ! ✅"}), 200
    else:
        return jsonify({"message": "Utilisateur non trouvé. 🛑"}), 404  # 404 = Not Found


@users.route('/v1/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user_route(user_id):
    user = get_user(user_id)
    if user:
        delete_user(user_id)
        return jsonify({"message": f"Utilisateur supprimé avec succès !"})
    else:
        return jsonify({"message": "Utilisateur non trouvé"}), 404