from flask import Blueprint, request, jsonify, session
from app.database import get_db
from models.reservation_model import add_reservation, get_reservations, delete_reservation, modify_reservation
from app.utils import token_required

reservation = Blueprint('reservation', __name__)

@reservation.route("/v1/reservations", methods=['POST'])
@token_required
def add_reservation_route():
    data = request.get_json()
    add_reservation(data['user_id'], data['boat_id'], data['fishing_trip_id'], data['date_reservation'], data['statut'], data['nbplace'], data['start_datetime'], data['end_datetime'], data['price'])
    return jsonify({"message": "reservation added succefuly !"}), 200

@reservation.route("/v1/reservations", methods=['GET'])
@token_required
def get_reservation_route():
    data = request.get_json()

    reservation_user_id = data["user_id"] if "user_id" in data else None
    reservation_boat_id = data["boat_id"] if "boat_id" in data else None
    reservation_fishing_trip_id = data["fishing_trip_id"] if "fishing_trip_id" in data else None
    reservation_statut = data["statut"] if "statut" in data else None
    reservation_start_datetime = data["start_datetime"] if "start_datetime" in data else None
    reservation_end_datetime = data["end_datetime"] if "end_datetime" in data else None
    reservations = get_reservations(user_id=reservation_user_id, boat_id=reservation_boat_id, fishing_trip_id=reservation_fishing_trip_id, statut=reservation_statut, start_datetime=reservation_start_datetime, end_datetime=reservation_end_datetime)
    if reservations:
        return jsonify({
            "reservations": reservations
        }), 200
    else:
        return jsonify({
            "reservations": []
        }), 404

@reservation.route("/v1/reservations/<int:reservation_id>", methods=['DELETE'])
@token_required
def delete_reservation_route(reservation_id):
    delete_reservation(reservation_id)
    response = jsonify({"message": "Reservation deleted !"})
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 200


@reservation.route("/v1/reservations/<int:reservation_id>", methods=['PUT'])
@token_required
def modify_reservation_route(reservation_id):
    data = request.get_json()

    success = modify_reservation(
        reservation_id=reservation_id,
        boat_id=data.get('boat_id'),
        fishing_trip_id=data.get('fishing_trip_id'),
        date_reservation=data.get('date_reservation'),
        start_datetime=data.get('start_datetime'),
        end_datetime=data.get('end_datetime')
    )

    if success:
        response = jsonify({"message": "Reservation modifiée avec succès !"})
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 200
    else:
        response = jsonify({"message": "Aucune réservation trouvée."})
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 404