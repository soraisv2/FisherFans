import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_instance = os.getenv("DB_INSTANCE")

def create_tables():
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    
    # Création de la table 'users'
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   lastName TEXT NOT NULL,
                   firstName TEXT NOT NULL,
                   birth_date DATE NOT NULL,
                   email TEXT NOT NULL UNIQUE,
                   phone TEXT NOT NULL UNIQUE,
                   address TEXT NOT NULL,
                   zip_code TEXT NOT NULL,
                   city TEXT NOT NULL,
                   spoken_languages TEXT NOT NULL,  -- Stocké sous forme de liste séparée par des virgules
                   avatar_url TEXT,
                   boat_license_number TEXT NOT NULL CHECK(LENGTH(boat_license_number) = 8),
                   insurance_number TEXT NOT NULL CHECK(LENGTH(insurance_number) = 12),
                   password TEXT NOT NULL
                   )''')

    # Création de la table 'boats'
    cursor.execute('''CREATE TABLE IF NOT EXISTS boats (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   type TEXT NOT NULL,
                   capacity INTEGER NOT NULL CHECK(capacity > 0),
                   location TEXT NOT NULL,
                   owner_id INTEGER NOT NULL,
                   FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
                   )''')

    # Création de la table 'fishing_trips'
    cursor.execute('''CREATE TABLE IF NOT EXISTS fishing_trips (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   date DATE NOT NULL,
                   location TEXT NOT NULL,
                   fishing_type TEXT NOT NULL,
                   boat_id INTEGER NOT NULL,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (boat_id) REFERENCES boats(id) ON DELETE CASCADE
                   )''')

    # Création de la table 'fishing_logs'
    cursor.execute('''CREATE TABLE IF NOT EXISTS fishing_logs (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   fishing_trip_id INTEGER NOT NULL,
                   fish_type TEXT NOT NULL,
                   quantity INTEGER NOT NULL CHECK(quantity > 0),
                   catch_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (fishing_trip_id) REFERENCES fishing_trips(id) ON DELETE CASCADE
                   )''')

    # Création de la table 'reservations'
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER NOT NULL,
                   fishing_trip_id INTEGER NOT NULL,
                   status TEXT CHECK(status IN ('pending', 'confirmed', 'canceled')) DEFAULT 'pending',
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                   FOREIGN KEY (fishing_trip_id) REFERENCES fishing_trips(id) ON DELETE CASCADE
                   )''')

    # Création de la table 'fishing_logs_pages'
    cursor.execute('''CREATE TABLE IF NOT EXISTS fishing_logs_pages (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER NOT NULL,
                   title TEXT NOT NULL,
                   content TEXT NOT NULL,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                   )''')

    conn.commit()
    conn.close()

# Exécution du script
create_tables()