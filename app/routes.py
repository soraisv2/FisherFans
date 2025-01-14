from flask import Blueprint, request, jsonify, session, redirect, url_for
from .database import get_db
from models.users import get_users, add_user, get_user, delete_user, modify_user, login_user
from models.boat_model import add_boat, get_boats

main = Blueprint('main', __name__)

#region deleteTable

@main.route('/delete_table', methods=['DELETE'])
def delete_table_route():
    if not request.is_json:
        return jsonify({"error": "Le contenu doit être en JSON"}), 415

    data = request.get_json()
    table_name = data.get("table_name")

    if not table_name:
        return jsonify({"error": "Nom de la table manquant."}), 400

    conn = get_db()
    cursor = conn.cursor()

    # Vérifie si la table existe avant de la supprimer
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    table_exists = cursor.fetchone()

    if not table_exists:
        return jsonify({"error": f"La table '{table_name}' n'existe pas."}), 400

    # Supprime la table
    cursor.execute(f"DROP TABLE {table_name}")
    conn.commit()
    conn.close()

    return jsonify({"message": f"Table '{table_name}' supprimée avec succès !"})

#endregion


#region Users

@main.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    user = login_user(data['email'], data['password'])
    if user:
        print(user)
        session['user_id'] = user[0]
        session['email'] = user[3]
        return jsonify({"message": "Users succefuly connected"}), 200
    else:
        return jsonify({"message": "Email ou mot de passe incorrect."}), 404


@main.route('/add_user', methods=['POST'])
def add_user_route():
    data = request.get_json()
    add_user(data['lastName'], data['firstName'], data['email'], data['password'], data['boat_license_number'])
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

@main.route('/get_user', methods=['GET'])
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

@main.route('/modify_user', methods=['PUT'])
def modify_user_route():
    data = request.get_json()
    user = get_user(data["user_id"])
    if user:
        modify_user(data['lastName'], data['firstName'], data['email'], data['boat_lisense_number'])
        return jsonify({"message": f"Utilisateur avec l'id {data['user_id']} modifié avec succès !"})
    else:
        return jsonify({"message": "Utilisateur non trouvé"}), 404

@main.route('/delete_user', methods=['DELETE'])
def delete_user_route():
    data = request.get_json()
    user = get_user(data["user_id"])
    if user:
        delete_user(data["user_id"])
        return jsonify({"message": f"Utilisateur avec l'id {data["user_id"]} supprimé avec succès !"})
    else:
        return jsonify({"message": "Utilisateur non trouvé"}), 404
    
#endregion

#region Boats

@main.route('/boat', methods=['POST'])
def add_boat_route():
    print(session)
    if 'user_id' not in session:
        return jsonify({"message": "You need to be connected to add a boat"}), 401
    data = request.get_json()
    add_boat(data['name'], data['type'], data['capacity'], data['location'])
    return jsonify({"message": "Boat added succefuly !"}), 200

@main.route('/boat', methods=['GET'])
def get_boat_route():
    data = request.get_json()

    boat_type = data["type"] if "type" in data else None
    boat_capacity = data["capacity"] if "capacity" in data else None
    boats = get_boats(type=boat_type, capacity=boat_capacity)
    if boats:
        return jsonify({
            "message": "Boats fetched successfully!",
            "boats": boats
        }), 200
    else:
        return jsonify({
            "message": "No boats found with the given filters.",
            "boats": []
        }), 404


#endregion
