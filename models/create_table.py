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
                    firstName TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    boat_license_number TEXT NOT NULL)''')

    # Création de la table 'boats'
    cursor.execute('''CREATE TABLE IF NOT EXISTS boats
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    longitude REAL NOT NULL,
                    latitude REAL NOT NULL,
                    capacity TEXT NOT NULL,
                    location TEXT NOT NULL,
                    longitude REAL NOT NULL,  -- Nouveau champ pour la longitude
                    latitude REAL NOT NULL,   -- Nouveau champ pour la latitude
                    owner_id INTEGER NOT NULL,
                    FOREIGN KEY (owner_id) REFERENCES users(id))''')

    # Création de la table 'fishing_trips'
    cursor.execute('''CREATE TABLE IF NOT EXISTS fishing_trips
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE NOT NULL,
                    location TEXT NOT NULL,
                    fishing_type TEXT NOT NULL,
                    boat_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (boat_id) REFERENCES boats(id))''')  

    # Création de la table 'fishing_logs'
    cursor.execute('''CREATE TABLE IF NOT EXISTS fishing_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fishing_trip_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (fishing_trip_id) REFERENCES fishing_trips(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )''')

    # Création de la table 'fishing_log_entries'
    cursor.execute('''CREATE TABLE IF NOT EXISTS fishing_log_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fishing_log_id INTEGER NOT NULL,
        fish_name TEXT NOT NULL,
        fish_photo_url TEXT,
        comment TEXT,
        size_cm REAL,
        weight_kg REAL,
        fishing_location TEXT NOT NULL,
        fishing_date DATE NOT NULL,
        fish_released BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (fishing_log_id) REFERENCES fishing_logs(id) ON DELETE CASCADE
    )''')

    # Création de la table 'reservation'
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservation
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    boat_id INTEGER NOT NULL,
                    fishing_trip_id INTEGER NOT NULL,
                    date_reservation TEXT NOT NULL,
                    statut TEXT NOT NULL,
                    nbplace INTEGER NOT NULL,
                    start_datetime TEXT NOT NULL,
                    end_datetime TEXT NOT NULL,
                    price FLOAT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (boat_id) REFERENCES boats(id),
                    FOREIGN KEY (fishing_trip_id) REFERENCES fishing_trips(id))''')

    conn.commit()
    conn.close()
