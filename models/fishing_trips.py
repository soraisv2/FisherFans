import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_instance = os.getenv("DB_INSTANCE")

if not db_instance:
    raise ValueError("DB_INSTANCE non configuré dans le fichier .env")

def add_fishing_trip(date, location, fishing_type, boat_id):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fishing_trips (date, location, fishing_type, boat_id) 
            VALUES (?, ?, ?, ?)
        """, (date, location, fishing_type, boat_id))
        conn.commit()

def get_fishing_trips(filters=None):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM fishing_trips"
        params = []

        if filters:
            conditions = []
            if "date" in filters:
                conditions.append("date = ?")
                params.append(filters["date"])
            if "fishing_type" in filters:
                conditions.append("fishing_type = ?")
                params.append(filters["fishing_type"])
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, params)
        trips = cursor.fetchall()
    return trips

def get_fishing_trip(trip_id):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fishing_trips WHERE id = ?", (trip_id,))
        trip = cursor.fetchone()
    return trip

def modify_fishing_trip(trip_id, date, location, fishing_type):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE fishing_trips 
            SET date = ?, location = ?, fishing_type = ?
            WHERE id = ?
        """, (date, location, fishing_type, trip_id))
        conn.commit()

def delete_fishing_trip(trip_id):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fishing_trips WHERE id = ?", (trip_id,))
        conn.commit()
