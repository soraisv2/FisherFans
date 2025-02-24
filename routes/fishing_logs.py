from flask import Blueprint, jsonify, request
from models.fishing_logs import get_fishing_logs, add_fishing_log, get_fishing_log, modify_fishing_log, delete_fishing_log


fishing_logs_bp = Blueprint('fishing_logs', __name__)

@fishing_logs_bp.route('/fishing_logs', methods=['GET'])
def get_fishing_logs():
    logs = get_fishing_logs()  # Récupération de tous les fishing logs depuis la base de données
    return jsonify(logs), 200

@fishing_logs_bp.route('/fishing_logs', methods=['POST'])
def create_fishing_log():
    data = request.get_json()
    # Logique pour créer un fishing log
    return jsonify({"message": "Fishing log created", "data": data}), 201

@fishing_logs_bp.route('/fishing_logs/<int:log_id>', methods=['GET'])
def get_fishing_log_route(log_id):
    log = fishing_logs.get_fishing_log(log_id)
    if log:
        response = jsonify(log)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 200
    response = jsonify({"error": "Fishing log not found"})
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 404

@fishing_logs_bp.route('/fishing_logs/<int:log_id>', methods=['PUT'])
def modify_fishing_log_route(log_id):
    data = request.get_json()

    fishing_logs.modify_fishing_log(
        log_id=log_id,
        title=data.get('title'),
        description=data.get('description')
    )
    response = jsonify({"message": "Fishing log updated successfully!"})
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 200

@fishing_logs_bp.route('/fishing_logs/<int:log_id>', methods=['DELETE'])
def delete_fishing_log_route(log_id):
    fishing_logs.delete_fishing_log(log_id)
    response = jsonify({"message": "Fishing log deleted successfully!"})
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 200
