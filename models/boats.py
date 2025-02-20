import sqlite3
import os
from dotenv import load_dotenv
from flask import request

load_dotenv()

db_instance = os.getenv("DB_INSTANCE")

def add_boat(name, type, capacity, location, owner_id):
    try:
        conn = sqlite3.connect(db_instance)
        cursor = conn.cursor()
        cursor.execute("SELECT boat_license_number FROM users WHERE id = ?", (owner_id,))
        result = cursor.fetchone()
        if not result or not result[0]:
            return False, "Boat license number not found for the user. 🛑"
        cursor.execute("INSERT INTO boats (name, type, capacity, location, owner_id) VALUES (?, ?, ?, ?, ?)", 
                    (name, type, capacity, location, owner_id))
        conn.commit()
        return True, "Boat added succefuly ! ✅"
    except:
        return False, "Error while adding boat 🛑"
    finally:
        if conn:
            conn.close()

def get_boats(type: str | None = None, capacity: int | None = None):
    try:
        conn = sqlite3.connect(db_instance)
        cursor = conn.cursor()
        query = "SELECT * FROM boats WHERE 1=1"
        params = []
        
        if type:
            query += " AND type = ?"
            params.append(type)
        if capacity:
            query += " AND capacity = ?"
            params.append(capacity)

        cursor.execute(query, tuple(params))
        boats = cursor.fetchall()
        return True, boats
    except:
        return False, None
    finally:
        if conn:
            conn.close()
