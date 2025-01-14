import sqlite3
import os
from dotenv import load_dotenv
from flask import session

load_dotenv()

db_instance = os.getenv("DB_INSTANCE")

def add_boat(name, type, capacity, location):
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    owner_id = session['user_id']
    cursor.execute("INSERT INTO boats (name, type, capacity, location, owner_id) VALUES (?, ?, ?, ?, ?)", 
                   (name, type, capacity, location, owner_id))
    conn.commit()
    conn.close()

def get_boats(type=None, capacity=None):
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    
    # Base de la requête SQL
    query = "SELECT * FROM boats WHERE 1=1"
    params = []
    
    # Ajouter des filtres dynamiquement
    if type:  # Si un type est fourni
        query += " AND type = ?"
        params.append(type)
    if capacity:  # Si une capacité est fournie
        query += " AND capacity = ?"
        params.append(capacity)
    
    # Exécuter la requête
    cursor.execute(query, tuple(params))
    boats = cursor.fetchall()
    
    conn.close()
    return boats
