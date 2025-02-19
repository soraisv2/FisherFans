from flask import Blueprint, request, jsonify, session, redirect, url_for, current_app
from app.database import get_db
from models.users import get_users, add_user, get_user, delete_user, modify_user, login_user
# JWT secure import
import jwt, datetime
from app.utils import token_required

users = Blueprint('users', __name__)

@users.route('/add_user', methods=['POST'])
def add_user_route():
    data = request.get_json()
    add_user(data['lastName'], data['firstName'], data['email'], data['password'], data['boat_license_number'])
    return jsonify({"message": "Utilisateur ajouté avec succès !"})

# @users.route('/login', methods=['POST'])
# def login_route():
#     data = request.get_json()
#     user = login_user(data['email'], data['password'])
#     if user:
#         session['user_id'] = user[0]
#         session['email'] = user[3]
#         return jsonify({"message": "Users succefuly connected"}), 200
#     else:
#         return jsonify({"message": "Email ou mot de passe incorrect."}), 404

@users.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()  # Récupère les données envoyées (email, password)
    user = login_user(data['email'], data['password'])  # Vérifie les identifiants en base
    if user:
        token = jwt.encode(
            {
                'user_id': user[0],  # ID utilisateur
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1) # Date d'expiration du token
            },
            current_app.config['SECRET_KEY'],  # Clé secrète pour signer le token
            algorithm='HS256'  # Algorithme de chiffrement
        )
        return jsonify({"message": "Utilisateur connecté avec succès", "token": token}), 200
    else:
        return jsonify({"message": "Email ou mot de passe incorrect."}), 404


@users.route('/get_users', methods=['GET'])
def get_users_route():
    users = get_users()
    user_list = []
    for user in users:
        user_dict = {
            "id": user[0],
            "nom": user[1],
            "prenom": user[2],
            "email": user[3],
            "mot_de_passe": user[4]
        }
        user_list.append(user_dict)
    return jsonify(user_list)

@users.route('/get_user', methods=['GET'])
@token_required
def get_user_route():
    data = request.get_json()
    user = get_user(data["user_id"])
    if user:
        user_dict = {
            "id": user[0],
            "nom": user[1],
            "prenom": user[2],
            "email": user[3],
            "mot_de_passe": user[4]
        }
        return jsonify(user_dict)
    else:
        return jsonify({"message": "Utilisateur non trouvé"}), 404

@users.route('/modify_user', methods=['PUT'])
def modify_user_route():
    data = request.get_json()
    user = get_user(data["user_id"])
    if user:
        modify_user(data['lastName'], data['firstName'], data['email'], data['boat_lisense_number'])
        return jsonify({"message": f"Utilisateur avec l'id {data['user_id']} modifié avec succès !"})
    else:
        return jsonify({"message": "Utilisateur non trouvé"}), 404

@users.route('/delete_user', methods=['DELETE'])
def delete_user_route():
    data = request.get_json()
    user = get_user(data["user_id"])
    if user:
        delete_user(data["user_id"])
        return jsonify({"message": f"Utilisateur avec l'id {data["user_id"]} supprimé avec succès !"})
    else:
        return jsonify({"message": "Utilisateur non trouvé"}), 404