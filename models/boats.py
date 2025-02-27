import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_instance = os.getenv("DB_INSTANCE")

if not db_instance:
    raise ValueError("DB_INSTANCE is not configured in the .env file")

def add_boat(name, type, capacity, location, owner_id, longitude, latitude):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO boats (name, type, capacity, location, owner_id, longitude, latitude) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, type, capacity, location, owner_id, longitude, latitude))
        conn.commit()
        
        boat_id = cursor.lastrowid
        
    return {
        "id": boat_id,
        "name": name,
        "type": type,
        "capacity": capacity,
        "location": location,
        "owner_id": owner_id
    }

def get_boats(filters=None):
    with sqlite3.connect(db_instance) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = """
            SELECT id, name, type, capacity, location, owner_id, longitude, latitude
            FROM boats
        """
        params = []

        if filters:
            conditions = []
            if "type" in filters:
                conditions.append("type = ?")
                params.append(filters["type"])
            if "capacity" in filters:
                conditions.append("capacity >= ?")
                params.append(filters["capacity"])
            if "owner_id" in filters:
                conditions.append("owner_id = ?")
                params.append(filters["owner_id"])
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, params)
        boats = cursor.fetchall()

        return [
            {
                "id": boat["id"],
                "name": boat["name"],
                "type": boat["type"],
                "capacity": boat["capacity"],
                "location": boat["location"],
                "owner_id": boat["owner_id"],
                "longitude": boat["longitude"],
                "latitude": boat["latitude"]
            }
            for boat in boats
        ]

def get_user_boats(user_id):
    filters = {"owner_id": user_id}
    boats = get_boats(filters)
    return boats

def get_boat(boat_id):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM boats WHERE id = ?", (boat_id,))
        boat = cursor.fetchone()
    return boat

def modify_boat(boat_id, name, type, capacity, location):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE boats 
            SET name = ?, type = ?, capacity = ?, location = ?
            WHERE id = ?
        """, (name, type, capacity, location, boat_id))
        conn.commit()

def delete_boat(boat_id):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM boats WHERE id = ?", (boat_id,))
        conn.commit()

def get_boats_by_zone(top_left, bottom_right):
    with sqlite3.connect(db_instance) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Requête SQL pour récupérer les bateaux dans la zone spécifiée
        query = """
            SELECT id, name, type, capacity, location, owner_id, longitude, latitude
            FROM boats
            WHERE latitude BETWEEN ? AND ?
            AND longitude BETWEEN ? AND ?
        """
        cursor.execute(query, (
            bottom_right["latitude"], top_left["latitude"],  # De haut en bas (correct)
            bottom_right["longitude"], top_left["longitude"]  # De gauche à droite (corrigé)
        ))


        boats = cursor.fetchall()
        return [
            {
                "id": boat["id"],
                "name": boat["name"],
                "type": boat["type"],
                "capacity": boat["capacity"],
                "location": boat["location"],
                "owner_id": boat["owner_id"],
                "longitude": boat["longitude"],
                "latitude": boat["latitude"]
            }
            for boat in boats
        ]

