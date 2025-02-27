import jwt
from functools import wraps
from flask import request, jsonify, current_app, g
import random
import math

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Récupère le token dans le header 'Authorization'
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'Token manquant 🛑'}), 401
        try:
            decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user = decoded  # Stocke les infos du token dans la requête
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expiré 🛑'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token invalide🛑'}), 401
        return f(*args, **kwargs)
    return decorated

def generate_random_location():
    lat_center = 43.5510
    lon_center = 7.0176
    distance_km=20
    # km en deg
    km_to_deg = 1 / 111.32  # Un degré de latitude correspond à environ 111.32 km.
    
    # Calcul de la distance maximale en latitude et longitude
    max_lat_distance = distance_km * km_to_deg
    max_lon_distance = distance_km * km_to_deg / abs(math.cos(math.radians(lat_center)))  # ajuster selon la latitude

    # Générer une latitude et longitude aléatoires dans la plage donnée
    lat_random = lat_center + random.uniform(-max_lat_distance, max_lat_distance)
    lon_random = lon_center + random.uniform(-max_lon_distance, max_lon_distance)

    # Vérifier si la position générée est sur la mer devant Cannes
    if lat_random > lat_center:  # Vérifie que c'est sur la mer (au sud de Cannes)
        return lat_random, lon_random
    else:
        return generate_random_location(lat_center, lon_center, distance_km)  # Reprendre si position invalide

# Coordonnées approximatives de Cannes
  # Latitude de Cannes
   # Longitude de Cannes