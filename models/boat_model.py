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