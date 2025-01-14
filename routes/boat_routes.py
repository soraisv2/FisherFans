from flask import Blueprint, request, jsonify, session
from app.database import get_db
from models.boat_model import add_boat, get_boats

boat = Blueprint('boat', __name__)

@boat.route('/boat', methods=['POST'])
def add_boat_route():
    if 'user_id' not in session:
        return jsonify({"message": "You need to be connected to add a boat"}), 401
    data = request.get_json()
    add_boat(data['name'], data['type'], data['capacity'], data['location'])
    return jsonify({"message": "Boat added succefuly !"}), 200

@boat.route('/boat', methods=['GET'])
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
