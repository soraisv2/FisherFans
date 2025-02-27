import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_instance = os.getenv("DB_INSTANCE")

def add_user(lastName, firstName, email, password, boat_license_number, date_of_birth, phone, address, postal_code, city, spoken_languages, avatar_url, insurance_number):
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()

    # Vérifier si l'email est déjà utilisé
    cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return False, "Cet email est déjà utilisé. 🛑"

    # Ajouter un nouvel utilisateur avec les champs supplémentaires
    cursor.execute("""
        INSERT INTO users (lastName, firstName, email, password, boat_license_number, date_of_birth, phone, address, postal_code, city, spoken_languages, avatar_url, insurance_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (lastName, firstName, email, password, boat_license_number, date_of_birth, phone, address, postal_code, city, ",".join(spoken_languages), avatar_url, insurance_number))

    conn.commit()
    conn.close()
    return True, "Utilisateur ajouté avec succès ! ✅"

def login_user(email, password):
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return True, user
    return False, None

def get_users():
    try:
        conn = sqlite3.connect(db_instance)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return True, users
    except sqlite3.Error:
        return False, None
    finally:
        if conn:
            conn.close()  

def get_user(user_id):
    try:
        conn = sqlite3.connect(db_instance)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    except sqlite3.Error:
        return None
    finally:
        if conn:
            conn.close()

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