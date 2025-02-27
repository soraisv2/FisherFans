from flask import Blueprint, jsonify, request
from models.fishing_logs import get_fishing_logs, add_fishing_log, delete_fishing_log, modify_fishing_log, get_fishing_log
from flask import Response
import json

fishing_logs_bp = Blueprint('fishing_logs', __name__)

@fishing_logs_bp.route('/fishing_logs', methods=['GET'])
def get_fishing_logs_route():
    filters = {}
    title = request.args.get('title')
    user_id = request.args.get('user_id')

    if title:
        filters['title'] = title
    if user_id:
        filters['user_id'] = user_id

    logs = get_fishing_logs(filters)
    response = Response(
        json.dumps(logs, indent=2, sort_keys=False),
        mimetype='application/json; charset=utf-8'
    )
    return response, 200


# Créer un nouveau log de pêche
@fishing_logs_bp.route('/fishing_logs', methods=['POST'])
def create_fishing_log():
    data = request.get_json()

    if not data or not data.get('title') or not data.get('user_id'):
        return jsonify({"message": "Title and user_id are required"}), 400

    title = data.get('title')
    description = data.get('description', '')
    user_id = data.get('user_id')

    existing_log = get_fishing_logs({"title": title, "user_id": user_id})
    if existing_log:
        return jsonify({"message": "Fishing log already exists for this user with the same title"}), 409

    try:
        new_log = add_fishing_log(
            title=title,
            description=description,
            user_id=user_id
        )
    except Exception as e:
        return jsonify({"message": f"Error creating fishing log: {str(e)}"}), 500

    return jsonify({"message": "Fishing log created", "data": new_log}), 201


@fishing_logs_bp.route('/fishing_logs/<int:log_id>', methods=['GET'])
def get_fishing_log_route(log_id):
    log = get_fishing_log(log_id)
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

    if not data.get('title') or not data.get('description'):
        return jsonify({"message": "Title and description are required to update"}), 400

    try:
        modify_fishing_log(
            log_id=log_id,
            title=data.get('title'),
            description=data.get('description')
        )
    except Exception as e:
        return jsonify({"message": f"Error updating fishing log: {str(e)}"}), 500

    response = jsonify({"message": "Fishing log updated successfully!"})
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response, 200


@fishing_logs_bp.route('/fishing_logs/<int:log_id>', methods=['DELETE'])
def delete_fishing_log_route(log_id):
    try:
        delete_fishing_log(log_id)
    except Exception as e:
        return jsonify({"message": f"Error deleting fishing log: {str(e)}"}), 500
    return jsonify({"message": "Fishing log deleted successfully!"}), 200
