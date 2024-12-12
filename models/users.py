import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_instance = os.getenv("DB_INSTANCE")

def add_user(lastName, firstName, email, password):
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (lastName, firstName, email, password) VALUES (?, ?, ?, ?)", 
                   (lastName, firstName, email, password))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users