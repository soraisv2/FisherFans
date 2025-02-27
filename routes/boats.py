from flask import Blueprint, jsonify, request, Response  
from models.boats import get_boats, add_boat, delete_boat, modify_boat, get_boat
import json
# JWT secure import
import jwt, datetime
from app.utils import token_required

boats = Blueprint('boats', __name__)

@boats.route("/v1/boats", methods=["GET"])
@token_required
def get_boats_route():
    filters = {}
    boat_type = request.args.get('type')
    capacity = request.args.get('capacity')

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

    required_fields = ["name", "type", "capacity", "location", "owner_id", "longitude", "latitude"]
    if not all(field in data for field in required_fields):
        return jsonify({"code": 400, "message": "Missing required fields"}), 400

    boat = add_boat(
        data["name"], data["type"], data["capacity"], data["location"], data["owner_id"], data["longitude"], data["latitude"]
    )

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

    # Vérification des autorisations avant de supprimer
    # Par exemple, si l'utilisateur n'est pas le propriétaire du bateau ou n'a pas les permissions
    # Cela dépend de la logique de ton application
    # if not user_has_permission_to_delete(boat_id):
    #     return jsonify({"code": 403, "message": "Forbidden - Not authorized to delete this boat"}), 403

    delete_boat(boat_id)
    return jsonify({"message": "Boat deleted successfully"}), 200