import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_instance = os.getenv("DB_INSTANCE")

def add_user(lastName, firstName, email, password, boat_license_number):
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (lastName, firstName, email, password, boat_license_number) VALUES (?, ?, ?, ?, ?)", 
                   (lastName, firstName, email, password, boat_license_number))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def get_user(user_id):
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def modify_user(user_id, lastName, firstName, email, boat_license_number):
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users 
        SET lastName = ?, firstName = ?, email = ?, boat_license_number = ?
        WHERE id = ?
    """, (lastName, firstName, email, boat_license_number, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()