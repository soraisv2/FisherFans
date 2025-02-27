from flask import Blueprint, request, jsonify, session, redirect, url_for, current_app
from app.database import get_db
from models.users import get_users, add_user, get_user, delete_user, modify_user, login_user
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
        if not all(k in data for k in ["lastName", "firstName", "email", "password", "boat_license_number"]):
            return jsonify({"message": "Missing registration fields. 🛑"}), 400

        success, message = add_user(
            data["lastName"], data["firstName"], data["email"], data["password"], data["boat_license_number"]
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



@users.route('/v1/users', methods=['GET'])
@token_required
def get_users_or_user():
    user_id = request.args.get("user_id")  # Récupération de l'ID via les paramètres d'URL

    if user_id:  # Si un ID est fourni, on récupère un seul utilisateur
        user = get_user(user_id)
        if user:
            user_dict = {
                "id": user[0],
                "nom": user[1],
                "prenom": user[2],
                "email": user[3],
                "mot_de_passe": user[4]
            }
            return jsonify(user_dict), 200
        else:
            return jsonify({"message": "Error while retrieving user. 🛑"}), 404
    else:  # Sinon, on récupère tous les utilisateurs
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


@users.route('/v1/users', methods=['PUT'])
@token_required
def modify_user_route():
    data = request.get_json()
    user = get_user(data["user_id"])
    if user:
        modify_user(data['lastName'], data['firstName'], data['email'], data['boat_lisense_number'])
        return jsonify({"message": f"Utilisateur avec l'id {data['user_id']} modifié avec succès !"})
    else:
        return jsonify({"message": "Utilisateur non trouvé"}), 404

@users.route('/v1/users', methods=['DELETE'])
@token_required
def delete_user_route():
    data = request.get_json()
    user = get_user(data["user_id"])
    if user:
        delete_user(data["user_id"])
        return jsonify({"message": f"Utilisateur supprimé avec succès !"})
    else:
        return jsonify({"message": "Utilisateur non trouvé"}), 404