from flask import Blueprint, request, jsonify

# Créer le blueprint
main = Blueprint('main', __name__)

@main.route('/health', methods=['GET'])
def health_check():
    """
    Vérifie si l'application fonctionne correctement.
    """
    return jsonify({"status": "OK"}), 200

@main.route('/example', methods=['GET'])
def example_route():
    """
    Une route d'exemple.
    """
    return jsonify({"message": "Bienvenue sur l'API FisherFans !"}), 200
