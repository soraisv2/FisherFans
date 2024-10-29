from flask import Blueprint, request, jsonify
from models import Utilisateur

utilisateurs_bp = Blueprint('utilisateurs', __name__)

@utilisateurs_bp.route('/utilisateurs', methods=['POST'])
def ajouter_utilisateur():
    from app import db  # Importer db ici pour éviter le problème de circular import
    data = request.get_json()
    nouvel_utilisateur = Utilisateur(nom=data['nom'], email=data['email'])
    db.session.add(nouvel_utilisateur)
    db.session.commit()
    return jsonify(nouvel_utilisateur.to_dict()), 201


# Get all users
@utilisateurs_bp.route('/', methods=['GET'])
def get_utilisateurs():
    utilisateurs = Utilisateur.query.all()
    return jsonify([u.to_dict() for u in utilisateurs])

# Get user by [id]
@utilisateurs_bp.route('/<int:id>', methods=['GET'])
def get_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    return jsonify(utilisateur.to_dict())

# Update user's data
@utilisateurs_bp.route('/<int:id>', methods=['PUT'])
def update_utilisateur(id):
    data = request.get_json()
    utilisateur = Utilisateur.query.get_or_404(id)
    utilisateur.nom = data['nom']
    utilisateur.email = data['email']
    db.session.commit()
    return jsonify({'message': 'Utilisateur modifié'})

# Delete user by [id]
@utilisateurs_bp.route('/<int:id>', methods=['DELETE'])
def delete_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    db.session.delete(utilisateur)
    db.session.commit()
    return jsonify({'message': 'Utilisateur supprimé'})
