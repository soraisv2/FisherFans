import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_instance = os.getenv("DB_INSTANCE")

def create_tables():
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    
    # Création de la table 'users'
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lastName TEXT NOT NULL,
                    firstName TEXT NOT NULL,  -- Modifié de INTEGER à TEXT pour 'firstName'
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    boat_license_number TEXT NOT NULL)''')
    
    # Création de la table 'boats'
    cursor.execute('''CREATE TABLE IF NOT EXISTS boats
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,  -- Modifié de INTEGER à TEXT pour 'type'
                    capacity TEXT NOT NULL,
                    location TEXT NOT NULL,
                    owner_id INTEGER NOT NULL)''')  # Changement de type de 'owner_id' de TEXT à INTEGER pour correspondre à l'ID de l'utilisateur
    
    # Création de la table 'fishing_trips'
    cursor.execute('''CREATE TABLE IF NOT EXISTS fishing_trips
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE NOT NULL,
                    location TEXT NOT NULL,
                    fishing_type TEXT NOT NULL,
                    boat_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()
