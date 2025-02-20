from flask import Blueprint, request, jsonify
from app.database import get_db
from models.boats import add_boat, get_boats
from app.utils import token_required

boat = Blueprint('boat', __name__)

@boat.route('/add_boat', methods=['POST'])
@token_required
def add_boat_route():

    data = request.get_json()
    print(request.user['user_id'])
    success, message = add_boat(data['name'], data['type'], data['capacity'], data['location'], request.user['user_id'])
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 400

@boat.route('/boat', methods=['GET'])
@token_required
def get_boat_route():
    data = request.get_json()
    boat_type = data["type"] if "type" in data else None
    boat_capacity = data["capacity"] if "capacity" in data else None
    success, boats = get_boats(type=boat_type, capacity=boat_capacity)
    if success:
        return jsonify({"boats": boats}), 200
    else:
        return jsonify({"message": "Error while retrieving boats 🛑",}), 400
