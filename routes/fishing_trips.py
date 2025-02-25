from flask import Blueprint, request, jsonify
from models import fishing_trips

fishing_trips_bp = Blueprint('fishing_trips', __name__)

@fishing_trips_bp.route('/', methods=['POST'])
def add_fishing_trip_route():
    data = request.get_json()
    fishing_trips.add_fishing_trip(
        date=data.get('date'),
        location=data.get('location'),
        fishing_type=data.get('fishing_type'),
        boat_id=data.get('boat_id')
    )
    response = jsonify({"message": "Fishing trip added successfully!"})
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 201

@fishing_trips_bp.route('/', methods=['GET'])
def get_fishing_trips_route():
    filters = request.args.to_dict()
    trips = fishing_trips.get_fishing_trips(filters)
    response = jsonify(trips)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 200

@fishing_trips_bp.route('/<int:trip_id>', methods=['GET'])
def get_fishing_trip_route(trip_id):
    trip = fishing_trips.get_fishing_trip(trip_id)
    if trip:
        response = jsonify(trip)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 200
    response = jsonify({"error": "Fishing trip not found"})
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 404

@fishing_trips_bp.route('/<int:trip_id>', methods=['PUT'])
def modify_fishing_trip_route(trip_id):
    data = request.get_json()

    fishing_trips.modify_fishing_trip(
        trip_id=trip_id,
        date=data.get('date'),
        location=data.get('location'),
        fishing_type=data.get('fishing_type')
    )
    
    response = jsonify({"message": "Fishing trip updated successfully!"})
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 200

@fishing_trips_bp.route('/<int:trip_id>', methods=['DELETE'])
def delete_fishing_trip_route(trip_id):
    fishing_trips.delete_fishing_trip(trip_id)
    response = jsonify({"message": "Fishing trip deleted successfully!"})
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 200
