from flask import Blueprint, jsonify, request, Response  
from models.boats import get_boats, add_boat, delete_boat, modify_boat, get_boat, get_boats_by_zone
from models.users import get_user
import json
# JWT secure import
import jwt, datetime
from app.utils import token_required

boats = Blueprint('boats', __name__)

@boats.route("/v1/boats", methods=["GET"])
@token_required
def get_boats_route():
    data = request.get_json()
    filters = {}
    boat_type = data["type"] if "type" in data else None
    capacity = data["capacity"] if "capacity" in data else None
    location = data["location"] if "location" in data else None
    
    if location:
        filters['location'] = location
    if boat_type:
        filters['type'] = boat_type
    if capacity:
        filters['capacity'] = capacity

    boats = get_boats(filters)
    response = Response(
        json.dumps(boats, indent=2, sort_keys=False),
        mimetype='application/json; charset=utf-8'
    )
    return response, 200

@boats.route("/v1/boats", methods=["POST"])
@token_required
def create_boat():
    data = request.get_json()
    user_id = request.user['user_id']

    required_fields = ["name", "type", "capacity", "location", "longitude", "latitude"]
    if not all(field in data for field in required_fields):
        return jsonify({"code": 400, "message": "Missing required fields"}), 400

    boat = add_boat(
        data["name"], data["type"], data["capacity"], data["location"], user_id, data["longitude"], data["latitude"]
    )

    user = get_user(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user[5]:
        return jsonify({"message": "Cannot add a boat because the user does not have a boat license number."}), 400

    if not boat:
        return jsonify({"message": "Failed to create boat"}), 500

    return jsonify({"message": "Boat created successfully"}), 201


@boats.route("/v1/boats/<int:boat_id>", methods=["GET"])
@token_required
def retrieve_boat(boat_id):
    boat = get_boat(boat_id)
    if boat:
        return jsonify(boat)
    return jsonify({"code": 404, "message": "Boat not found"}), 404

@boats.route("/v1/boats/<int:boat_id>", methods=["PUT"])
@token_required
def update_boat(boat_id):
    data = request.get_json()

    required_fields = ["name", "type", "capacity", "location"]
    if not all(field in data for field in required_fields):
        return jsonify({"code": 400, "message": "Missing required fields"}), 400

    boat = get_boat(boat_id)
    if not boat:
        return jsonify({"code": 404, "message": "Boat not found"}), 404

    modify_boat(boat_id, data["name"], data["type"], data["capacity"], data["location"])
    return jsonify({"message": "Boat updated successfully"}), 200

@boats.route("/v1/boats/<int:boat_id>", methods=["DELETE"])
@token_required
def remove_boat(boat_id):
    boat = get_boat(boat_id)
    if not boat:
        return jsonify({"code": 404, "message": "Boat not found"}), 404

    delete_boat(boat_id)
    return jsonify({"message": "Boat deleted successfully"}), 200

@boats.route("/v1/boats_by_geo", methods=["GET"])
@token_required
def boats_by_geo():
    data = request.get_json()
    top_left = data['top_left']
    bottom_right = data['bottom_right']

    if not top_left["longitude"] or not top_left["latitude"] or not bottom_right["longitude"] or not bottom_right["latitude"]:
        return jsonify({"code": 400, "message": "Missing required fields"}), 400

    boats = get_boats_by_zone(top_left, bottom_right)
    response = Response(
        json.dumps(boats, indent=2, sort_keys=False),
        mimetype='application/json; charset=utf-8'
    )
    return response, 200