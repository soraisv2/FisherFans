from flask import Blueprint, request, jsonify, session
from app.database import get_db
from models.reservation_model import add_reservation, get_reservations

reservation = Blueprint('reservation', __name__)

@reservation.route('/reservation', methods=['POST'])
def add_reservation_route():
    if 'user_id' not in session:
        return jsonify({"message": "You need to be connected to add a reservation"}), 401
    data = request.get_json()
    add_reservation(data['utilisateur_id'], data['bateau_id'], data['sortie_peche_id'], data['date_reservation'], data['statut'], data['start_datetime'], data['end_datetime'])
    return jsonify({"message": "reservation added succefuly !"}), 200

@reservation.route('/reservation', methods=['GET'])
def get_reservation_route():
    data = request.get_json()

    reservation_utilisateur_id = data["utilisateur_id"] if "utilisateur_id" in data else None
    reservation_bateau_id = data["bateau_id"] if "bateau_id" in data else None
    reservation_sortie_peche_id = data["sortie_peche_id"] if "sortie_peche_id" in data else None
    reservation_statut = data["statut"] if "statut" in data else None
    reservation_start_datetime = data["start_datetime"] if "start_datetime" in data else None
    reservation_end_datetime = data["end_datetime"] if "end_datetime" in data else None
    reservations = get_reservations(utilisateur_id=reservation_utilisateur_id, bateau_id=reservation_bateau_id, sortie_peche_id=reservation_sortie_peche_id, statut=reservation_statut, start_datetime=reservation_start_datetime, end_datetime=reservation_end_datetime)
    if reservations:
        return jsonify({
            "reservations": reservations
        }), 200
    else:
        return jsonify({
            "reservations": []
        }), 404
