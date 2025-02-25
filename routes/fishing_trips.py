from flask import Blueprint, request, jsonify, Response
from models.fishing_trips import add_fishing_trip, get_fishing_trips, modify_fishing_trip, delete_fishing_trip, get_fishing_trip
import json

# Définir le blueprint
fishing_trips_bp = Blueprint('fishing_trips', __name__)

@fishing_trips_bp.route('/fishing_trips', methods=['POST'])
def create_fishing_trip():
    data = request.get_json()
    date = data.get('date')
    location = data.get('location')
    fishing_type = data.get('fishing_type')
    boat_id = data.get('boat_id')

    # Vérifier si la sortie de pêche existe déjà
    existing_trip = get_fishing_trips({"date": date, "location": location, "fishing_type": fishing_type})
    if existing_trip:
        return jsonify({"message": "Fishing trip already exists"}), 409  # Conflict

    # Ajouter la sortie de pêche
    add_fishing_trip(date, location, fishing_type, boat_id)
    
    # Récupérer le nouveau voyage de pêche
    new_trip = get_fishing_trips({"date": date, "location": location, "fishing_type": fishing_type})[0]
    
    # Structurer la réponse sans encapsulation
    response_data = {
        "id": new_trip["id"],
        "date": new_trip["date"],
        "location": new_trip["location"],
        "fishing_type": new_trip["fishing_type"],
        "boat_id": new_trip["boat_id"]
    }
    
    # Retourner la réponse JSON avec l'ordre des clés préservé
    return jsonify(response_data), 201  # Created

@fishing_trips_bp.route('/fishing_trips', methods=['GET'])
def get_all_fishing_trips():
    filters = {}
    if 'date' in request.args:
        filters['date'] = request.args['date']
    if 'fishing_type' in request.args:
        filters['fishing_type'] = request.args['fishing_type']
    
    trips = get_fishing_trips(filters)
    
    # Structurer la réponse sans encapsulation
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
    
    # Retourner la réponse JSON avec l'ordre des clés préservé
    return jsonify(response_data), 200

@fishing_trips_bp.route('/fishing_trips/<int:trip_id>', methods=['GET'])
def get_fishing_trip_route(trip_id):
    trip = get_fishing_trip(trip_id)
    if trip:
        # Structurer la réponse sans encapsulation
        response_data = {
            "id": trip["id"],
            "date": trip["date"],
            "location": trip["location"],
            "fishing_type": trip["fishing_type"],
            "boat_id": trip["boat_id"]
        }
        
        return jsonify(response_data), 200
    return jsonify({"message": "Fishing trip not found"}), 404

@fishing_trips_bp.route('/fishing_trips/<int:trip_id>', methods=['PUT'])
def update_fishing_trip(trip_id):
    data = request.get_json()
    date = data.get('date')
    location = data.get('location')
    fishing_type = data.get('fishing_type')

    # Vérifier si la sortie de pêche existe
    trip = get_fishing_trip(trip_id)
    if not trip:
        return jsonify({"message": "Fishing trip not found"}), 404

    # Modifier la sortie de pêche
    modify_fishing_trip(trip_id, date, location, fishing_type)
    
    # Structurer la réponse sans encapsulation
    updated_trip = get_fishing_trip(trip_id)
    response_data = {
        "id": updated_trip["id"],
        "date": updated_trip["date"],
        "location": updated_trip["location"],
        "fishing_type": updated_trip["fishing_type"],
        "boat_id": updated_trip["boat_id"]
    }
    
    return jsonify(response_data), 200

@fishing_trips_bp.route('/fishing_trips/<int:trip_id>', methods=['DELETE'])
def delete_fishing_trip_route(trip_id):
    # Vérifier si la sortie de pêche existe
    trip = get_fishing_trip(trip_id)
    if not trip:
        return jsonify({"message": "Fishing trip not found"}), 404

    # Supprimer la sortie de pêche
    delete_fishing_trip(trip_id)
    return jsonify({"message": "Fishing trip deleted successfully"}), 200
