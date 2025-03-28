import sqlite3
import os
from dotenv import load_dotenv
from flask import session, jsonify

load_dotenv()

db_instance = os.getenv("DB_INSTANCE")

def add_reservation(user_id, boat_id, fishing_trip_id, date_reservation, statut, nbplace, start_datetime, end_datetime, price):
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO reservation 
                      (user_id, boat_id, fishing_trip_id, date_reservation, statut, nbplace, start_datetime, end_datetime, price)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (user_id, boat_id, fishing_trip_id, date_reservation, statut, nbplace, start_datetime, end_datetime, price))
    
    conn.commit()
    conn.close()

def get_reservations(user_id=None, boat_id=None, fishing_trip_id=None, statut=None, start_datetime=None, end_datetime=None):
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()
    
    query = "SELECT * FROM reservation WHERE 1=1"
    params = []
    
    if user_id:
        query += " AND user_id = ?"
        params.append(user_id)
    if boat_id:
        query += " AND boat_id = ?"
        params.append(boat_id)
    if fishing_trip_id:
        query += " AND fishing_trip_id = ?"
        params.append(fishing_trip_id)
    if statut:
        query += " AND statut = ?"
        params.append(statut)
    if start_datetime:
        query += " AND start_datetime >= ?"
        params.append(start_datetime)
    if end_datetime:
        query += " AND end_datetime <= ?"
        params.append(end_datetime)
    
    cursor.execute(query, tuple(params))
    reservations = cursor.fetchall()
    
    conn.close()
    return reservations

def modify_reservation(reservation_id, boat_id, fishing_trip_id, date_reservation, start_datetime, end_datetime):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()

        # Vérifier si la réservation existe
        cursor.execute("SELECT * FROM reservation WHERE id = ?", (reservation_id,))
        reservation = cursor.fetchone()

        if not reservation:
            print(f"Reservation avec ID {reservation_id} non trouvée.")  # Log pour vérifier si l'ID existe
            return False

        # Log pour vérifier les valeurs actuelles et les nouvelles valeurs
        print(f"Anciennes valeurs : boat_id={reservation[1]}, fishing_trip_id={reservation[2]}, date_reservation={reservation[3]}, start_datetime={reservation[4]}, end_datetime={reservation[5]}")
        
        # Récupérer les valeurs actuelles de la réservation
        current_boat_id = reservation[1]
        current_fishing_trip_id = reservation[2]
        current_date_reservation = reservation[3]
        current_start_datetime = reservation[4]
        current_end_datetime = reservation[5]

        # Si la valeur est None, conserver la valeur actuelle
        if boat_id is None:
            boat_id = current_boat_id
        if fishing_trip_id is None:
            fishing_trip_id = current_fishing_trip_id
        if date_reservation is None:
            date_reservation = current_date_reservation
        if start_datetime is None:
            start_datetime = current_start_datetime
        if end_datetime is None:
            end_datetime = current_end_datetime

        # Log avant la mise à jour
        print(f"Mise à jour avec : boat_id={boat_id}, fishing_trip_id={fishing_trip_id}, date_reservation={date_reservation}, start_datetime={start_datetime}, end_datetime={end_datetime}")
        
        # Effectuer la mise à jour
        cursor.execute("""
            UPDATE reservation
            SET boat_id = ?, fishing_trip_id = ?, date_reservation = ?, start_datetime = ?, end_datetime = ?
            WHERE id = ?
        """, (boat_id, fishing_trip_id, date_reservation, start_datetime, end_datetime, reservation_id))

        conn.commit()

        # Log pour vérifier si la mise à jour a affecté des lignes
        if cursor.rowcount > 0:
            print(f"Réservation avec ID {reservation_id} mise à jour.")
            return True
        else:
            print(f"Aucune ligne affectée pour la réservation avec ID {reservation_id}.")
            return False
            

def delete_reservation(reservation_id):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reservation WHERE id = ?", (reservation_id,))
        conn.commit()