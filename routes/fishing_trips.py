from flask import Blueprint, request, jsonify
from models.fishing_trips import add_fishing_trip, get_fishing_trips, modify_fishing_trip, delete_fishing_trip, get_fishing_trip

# Définir le blueprint
fishing_trips_bp = Blueprint('fishing_trips', __name__)

# Route pour ajouter une sortie de pêche
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

    add_fishing_trip(date, location, fishing_type, boat_id)
    return jsonify({"message": "Fishing trip added successfully"}), 201

# Route pour obtenir toutes les sorties de pêche (avec des filtres optionnels)
@fishing_trips_bp.route('/fishing_trips', methods=['GET'])
def get_all_fishing_trips():
    filters = {}
    if 'date' in request.args:
        filters['date'] = request.args['date']
    if 'fishing_type' in request.args:
        filters['fishing_type'] = request.args['fishing_type']
    
    trips = get_fishing_trips(filters)
    return jsonify(trips)

# Route pour obtenir une sortie de pêche spécifique
@fishing_trips_bp.route('/fishing_trips/<int:trip_id>', methods=['GET'])
def get_fishing_trip_route(trip_id):
    trip = get_fishing_trip(trip_id)
    if trip:
        return jsonify(trip)
    return jsonify({"message": "Fishing trip not found"}), 404

# Route pour modifier une sortie de pêche
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

    modify_fishing_trip(trip_id, date, location, fishing_type)
    return jsonify({"message": "Fishing trip updated successfully"}), 200

# Route pour supprimer une sortie de pêche
@fishing_trips_bp.route('/fishing_trips/<int:trip_id>', methods=['DELETE'])
def delete_fishing_trip(trip_id):
    # Vérifier si la sortie de pêche existe
    trip = get_fishing_trip(trip_id)
    if not trip:
        return jsonify({"message": "Fishing trip not found"}), 404

    delete_fishing_trip(trip_id)
    return jsonify({"message": "Fishing trip deleted successfully"}), 200
