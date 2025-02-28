from flask import Blueprint, jsonify, request
from models.fishing_logs import (
    get_fishing_logs, add_fishing_log, delete_fishing_log, 
    modify_fishing_log, get_fishing_log, add_fishing_log_entry,
    update_fishing_log_entry, delete_fishing_log_entry, fishing_trip_exists
)
from flask import Response
import json
from app.utils import token_required

fishing_logs_bp = Blueprint('fishing_logs', __name__)

@fishing_logs_bp.route('/v1/fishing_logs', methods=['GET'])
@token_required
def get_fishing_logs_route():
    try:
        filters = {}
        title = request.args.get('title')
        user_id = request.args.get('user_id')

        if title:
            filters['title'] = title
        if user_id:
            try:
                filters['user_id'] = int(user_id)
            except ValueError:
                return jsonify({
                    "code": 400,
                    "message": "Invalid user_id format"
                }), 400

        logs = get_fishing_logs(filters)
        return jsonify(logs), 200
    except Exception as e:
        return jsonify({
            "code": 400,
            "message": f"Invalid request: {str(e)}"
        }), 400

@fishing_logs_bp.route('/v1/fishing_logs', methods=['POST'])
@token_required
def create_fishing_log():
    try:
        data = request.get_json()

        if not data or not isinstance(data, dict):
            return jsonify({
                "code": 400,
                "message": "Invalid request body"
            }), 400

        required_fields = ['title', 'user_id', 'fishing_trip_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "code": 400,
                    "message": f"Missing required field: {field}"
                }), 400

        # Vérification que fishing_trip_id existe en base
        if not fishing_trip_exists(data['fishing_trip_id']):
            return jsonify({
                "code": 400,
                "message": "Invalid fishing_trip_id: no matching trip found"
            }), 400

        new_log = add_fishing_log(
            title=data['title'],
            description=data.get('description', ''),
            user_id=data['user_id'],
            fishing_trip_id=data['fishing_trip_id']  # Ajout du champ
        )
        
        return jsonify(new_log), 201

    except Exception as e:
        return jsonify({
            "code": 400,
            "message": f"Invalid request: {str(e)}"
        }), 400


@fishing_logs_bp.route('/v1/fishing_logs/<int:log_id>', methods=['GET'])
@token_required
def get_fishing_log_route(log_id):
    log = get_fishing_log(log_id)
    if log:
        return jsonify(log), 200
    return jsonify({
        "code": 404,
        "message": "Fishing log not found"
    }), 404

@fishing_logs_bp.route('/v1/fishing_logs/<int:log_id>', methods=['PUT'])
@token_required
def modify_fishing_log_route(log_id):
    try:
        data = request.get_json()

        if not data or not isinstance(data, dict):
            return jsonify({
                "code": 400,
                "message": "Invalid request body"
            }), 400

        if 'title' not in data or 'description' not in data:
            return jsonify({
                "code": 400,
                "message": "Title and description are required"
            }), 400

        log = modify_fishing_log(
            log_id=log_id,
            title=data['title'],
            description=data['description']
        )
        
        if not log:
            return jsonify({
                "code": 404,
                "message": "Fishing log not found"
            }), 404

        return jsonify(log), 200
    except Exception as e:
        return jsonify({
            "code": 400,
            "message": f"Invalid request: {str(e)}"
        }), 400

@fishing_logs_bp.route('/v1/fishing_logs/<int:log_id>', methods=['DELETE'])
@token_required
def delete_fishing_log_route(log_id):
    try:
        log = get_fishing_log(log_id)
        if not log:
            return jsonify({
                "code": 404,
                "message": "Fishing log not found"
            }), 404

        delete_fishing_log(log_id)
        return '', 204
    except Exception as e:
        return jsonify({
            "code": 400,
            "message": f"Invalid request: {str(e)}"
        }), 400

@fishing_logs_bp.route('/v1/fishing_logs/<int:log_id>/entries', methods=['POST'])
@token_required
def create_fishing_log_entry(log_id):
    try:
        data = request.get_json()

        if not data or not isinstance(data, dict):
            return jsonify({
                "code": 400,
                "message": "Invalid request body"
            }), 400

        required_fields = ['fish_name', 'fishing_location', 'fishing_date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "code": 400,
                    "message": f"Missing required field: {field}"
                }), 400

        # Verify fishing log exists
        log = get_fishing_log(log_id)
        if not log:
            return jsonify({
                "code": 404,
                "message": "Fishing log not found"
            }), 404

        entry_id = add_fishing_log_entry(log_id, data)
        if entry_id:
            return jsonify({
                "id": entry_id,
                **data,
                "fishing_log_id": log_id
            }), 201
        
        return jsonify({
            "code": 400,
            "message": "Failed to create entry"
        }), 400
    except Exception as e:
        return jsonify({
            "code": 400,
            "message": f"Invalid request: {str(e)}"
        }), 400

@fishing_logs_bp.route('/v1/fishing_logs/<int:log_id>/entries/<int:entry_id>', methods=['PUT'])
@token_required
def update_fishing_log_entry_route(log_id, entry_id):
    try:
        data = request.get_json()

        if not data or not isinstance(data, dict):
            return jsonify({
                "code": 400,
                "message": "Invalid request body"
            }), 400

        result = update_fishing_log_entry(log_id, entry_id, data)
        if result is None:
            return jsonify({
                "code": 404,
                "message": "Fishing log or entry not found"
            }), 404

        return jsonify({
            "id": entry_id,
            **data,
            "fishing_log_id": log_id
        }), 200
    except Exception as e:
        return jsonify({
            "code": 400,
            "message": f"Invalid request: {str(e)}"
        }), 400

@fishing_logs_bp.route('/v1/fishing_logs/<int:log_id>/entries/<int:entry_id>', methods=['DELETE'])
@token_required
def delete_fishing_log_entry_route(log_id, entry_id):
    try:
        if delete_fishing_log_entry(log_id, entry_id):
            return '', 204
        return jsonify({
            "code": 404,
            "message": "Fishing log or entry not found"
        }), 404
    except Exception as e:
        return jsonify({
            "code": 400,
            "message": f"Invalid request: {str(e)}"
        }), 400