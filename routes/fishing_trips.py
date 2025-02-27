from flask import Blueprint, request, jsonify, Response
from models.fishing_trips import add_fishing_trip, get_fishing_trips, modify_fishing_trip, delete_fishing_trip, get_fishing_trip
from models.users import get_user
from models.boats import get_user_boats
import json
from app.utils import token_required

fishing_trips_bp = Blueprint('fishing_trips', __name__)

@fishing_trips_bp.route('/v1/fishing_trips', methods=['POST'])
@token_required
def create_fishing_trip():
    user_id = request.user['user_id']
    boats = get_user_boats(user_id)  # Récupère la liste des bateaux concernant l'utilisateur
    if boats == []:
        return jsonify({"message": "Cannot create a fishing log because the user does not have create boats."}), 400
    data = request.get_json()
    date = data.get('date')
    location = data.get('location')
    fishing_type = data.get('fishing_type')
    boat_id = data.get('boat_id')

    existing_trip = get_fishing_trips({"date": date, "location": location, "fishing_type": fishing_type})
    if existing_trip:
        return jsonify({"message": "Fishing trip already exists"}), 409

    add_fishing_trip(date, location, fishing_type, boat_id)
    
    new_trip = get_fishing_trips({"date": date, "location": location, "fishing_type": fishing_type})[0]
    
    response_data = {
        "id": new_trip["id"],
        "date": new_trip["date"],
        "location": new_trip["location"],
        "fishing_type": new_trip["fishing_type"],
        "boat_id": new_trip["boat_id"]
    }
    
    return jsonify(response_data), 201

@fishing_trips_bp.route('/v1/fishing_trips', methods=['GET'])
@token_required
def get_all_fishing_trips():
    filters = {}
    if 'date' in request.args:
        filters['date'] = request.args['date']
    if 'fishing_type' in request.args:
        filters['fishing_type'] = request.args['fishing_type']
    
    trips = get_fishing_trips(filters)
    
    response_data = [
        {
            "id": trip["id"],
            "date": trip["date"],
            "location": trip["location"],
            "fishing_type": trip["fishing_type"],
            "boat_id": trip["boat_id"]
        }
        for trip in trips
    ]
    
    return jsonify(response_data), 200

@fishing_trips_bp.route('/v1/fishing_trips/<int:trip_id>', methods=['GET'])
@token_required
def get_fishing_trip_route(trip_id):
    trip = get_fishing_trip(trip_id)
    if trip:
        response_data = {
            "id": trip["id"],
            "date": trip["date"],
            "location": trip["location"],
            "fishing_type": trip["fishing_type"],
            "boat_id": trip["boat_id"]
        }
        
        return jsonify(response_data), 200
    return jsonify({"message": "Fishing trip not found"}), 404

@fishing_trips_bp.route('/v1/fishing_trips/<int:trip_id>', methods=['PUT'])
@token_required
def update_fishing_trip(trip_id):
    data = request.get_json()
    date = data.get('date')
    location = data.get('location')
    fishing_type = data.get('fishing_type')

    trip = get_fishing_trip(trip_id)
    if not trip:
        return jsonify({"message": "Fishing trip not found"}), 404

    modify_fishing_trip(trip_id, date, location, fishing_type)
    
    updated_trip = get_fishing_trip(trip_id)
    response_data = {
        "id": updated_trip["id"],
        "date": updated_trip["date"],
        "location": updated_trip["location"],
        "fishing_type": updated_trip["fishing_type"],
        "boat_id": updated_trip["boat_id"]
    }
    
    return jsonify(response_data), 200

@fishing_trips_bp.route('/v1/fishing_trips/<int:trip_id>', methods=['DELETE'])
@token_required
def delete_fishing_trip_route(trip_id):
    trip = get_fishing_trip(trip_id)
    if not trip:
        return jsonify({"message": "Fishing trip not found"}), 404

    delete_fishing_trip(trip_id)
    return jsonify({"message": "Fishing trip deleted successfully"}), 200
