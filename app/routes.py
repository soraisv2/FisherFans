from flask import Blueprint, request, jsonify
from .database import get_db
from models.users import get_users, add_user

main = Blueprint('main', __name__)

@main.route('/add_user', methods=['POST'])
def add_user_route():
    data = request.get_json()
    add_user(data['lastName'], data['firstName'], data['email'], data['password'])
    return jsonify({"message": "Utilisateur ajouté avec succès !"})

@main.route('/get_users', methods=['GET'])
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