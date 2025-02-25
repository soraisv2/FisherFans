import sqlite3
import os
from dotenv import load_dotenv
from flask import session

load_dotenv()

db_instance = os.getenv("DB_INSTANCE")

def add_reservation(utilisateur_id, bateau_id, sortie_peche_id, date_reservation, statut, nbplace, start_datetime, end_datetime, price):
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO reservation 
                      (utilisateur_id, bateau_id, sortie_peche_id, date_reservation, statut, nbplace, start_datetime, end_datetime, price)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (utilisateur_id, bateau_id, sortie_peche_id, date_reservation, statut, nbplace, start_datetime, end_datetime, price))
    
    conn.commit()
    conn.close()

def get_reservations(utilisateur_id=None, bateau_id=None, sortie_peche_id=None, statut=None, start_datetime=None, end_datetime=None):
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    
    query = "SELECT * FROM reservation WHERE 1=1"
    params = []
    
    if utilisateur_id:
        query += " AND utilisateur_id = ?"
        params.append(utilisateur_id)
    if bateau_id:
        query += " AND bateau_id = ?"
        params.append(bateau_id)
    if sortie_peche_id:
        query += " AND sortie_peche_id = ?"
        params.append(sortie_peche_id)
    if statut:
        query += " AND statut = ?"
        params.append(statut)
    if start_datetime:
        query += " AND start_datetime >= ?"
        params.append(start_datetime)
    if end_datetime:
        query += " AND end_datetime <= ?"
        params.append(end_datetime)
    
    # Exécution de la requête avec les filtres
    cursor.execute(query, tuple(params))
    reservations = cursor.fetchall()
    
    conn.close()
    return reservations

def modify_reservation(reservation_id, bateau_id, sortie_id, date_reservation, start_datetime, end_datetime):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE reservation
            SET bateau_id = ?, sortie_id = ?, date_reservation = ?, start_datetime = ?, end_datetime = ?
            WHERE id = ?
        """, (bateau_id, sortie_id, date_reservation, start_datetime, end_datetime, reservation_id))
        conn.commit()

def delete_reservation(reservation_id):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reservation WHERE id = ?", (reservation_id,))
        conn.commit()