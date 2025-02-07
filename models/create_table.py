import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_instance = os.getenv("DB_INSTANCE")

def create_tables():
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lastName TEXT NOT NULL,
                    firstName INTEGER NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    boat_license_number TEXT NOT NULL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS boats
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type INTEGER NOT NULL,
                    capacity TEXT NOT NULL,
                    location TEXT NOT NULL,
                    owner_id TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS reservation
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    utilisateur_id INTEGER NOT NULL,
                    bateau_id INTEGER NOT NULL,
                    sortie_peche_id INTEGER NOT NULL,
                    date_reservation TEXT NOT NULL,
                    statut TEXT NOT NULL,
                    start_datetime TEXT NOT NULL,
                    end_datetime TEXT NOT NULL,
                    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id),
                    FOREIGN KEY (bateau_id) REFERENCES bateau(id),
                    FOREIGN KEY (sortie_peche_id) REFERENCES sortie_peche(id))''')

    conn.commit()
    conn.close()