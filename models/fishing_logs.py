import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
db_instance = os.getenv("DB_INSTANCE")

if not db_instance:
    raise ValueError("DB_INSTANCE is not configured in the .env file")

def add_fishing_log(title, description, user_id, fishing_trip_id):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fishing_logs (title, description, user_id, fishing_trip_id, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, user_id, fishing_trip_id, current_time, current_time))
        conn.commit()
        
        log_id = cursor.lastrowid
        
    return get_fishing_log(log_id)

def get_fishing_logs(filters=None):
    with sqlite3.connect(db_instance) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT fl.id, fl.title, fl.description, fl.created_at, fl.updated_at, fl.user_id 
            FROM fishing_logs fl
        """
        params = []

        if filters:
            conditions = []
            if "user_id" in filters:
                conditions.append("fl.user_id = ?")
                params.append(filters["user_id"])
            if "title" in filters:
                conditions.append("fl.title LIKE ?")
                params.append(f"%{filters['title']}%")
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, params)
        logs = cursor.fetchall()
        
        result = []
        for log in logs:
            log_dict = {
                "id": log["id"],
                "title": log["title"],
                "description": log["description"],
                "created_at": log["created_at"],
                "updated_at": log["updated_at"],
                "user_id": log["user_id"],
                "entries": get_fishing_log_entries(log["id"])
            }
            result.append(log_dict)
            
        return result

def get_fishing_log(log_id):
    with sqlite3.connect(db_instance) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, description, created_at, updated_at, user_id 
            FROM fishing_logs 
            WHERE id = ?
        """, (log_id,))
        log = cursor.fetchone()
        
        if log:
            return {
                "id": log["id"],
                "title": log["title"],
                "description": log["description"],
                "created_at": log["created_at"],
                "updated_at": log["updated_at"],
                "user_id": log["user_id"],
                "entries": get_fishing_log_entries(log_id)
            }
        return None

def modify_fishing_log(log_id, title, description):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE fishing_logs 
            SET title = ?, description = ?, updated_at = ?
            WHERE id = ?
        """, (title, description, current_time, log_id))
        conn.commit()
        
    return get_fishing_log(log_id)

def delete_fishing_log(log_id):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        # Delete associated entries first
        cursor.execute("DELETE FROM fishing_log_entries WHERE fishing_log_id = ?", (log_id,))
        # Then delete the log
        cursor.execute("DELETE FROM fishing_logs WHERE id = ?", (log_id,))
        conn.commit()

def get_fishing_log_entries(log_id):
    with sqlite3.connect(db_instance) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM fishing_log_entries 
            WHERE fishing_log_id = ?
        """, (log_id,))
        entries = cursor.fetchall()
        
        return [dict(entry) for entry in entries]

def add_fishing_log_entry(fishing_log_id, entry_data):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fishing_log_entries (
                fishing_log_id, fish_name, fish_photo_url, comment,
                size_cm, weight_kg, fishing_location, fishing_date,
                fish_released, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fishing_log_id, entry_data['fish_name'],
            entry_data.get('fish_photo_url'), entry_data.get('comment'),
            entry_data.get('size_cm'), entry_data.get('weight_kg'),
            entry_data['fishing_location'], entry_data['fishing_date'],
            entry_data.get('fish_released', False),
            current_time, current_time
        ))
        conn.commit()
        return cursor.lastrowid

def update_fishing_log_entry(log_id, entry_id, entry_data):
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        
        # Construct UPDATE query dynamically based on provided fields
        update_fields = []
        params = []
        for key in ['fish_name', 'fish_photo_url', 'comment', 'size_cm',
                   'weight_kg', 'fishing_location', 'fishing_date', 'fish_released']:
            if key in entry_data:
                update_fields.append(f"{key} = ?")
                params.append(entry_data[key])
        
        update_fields.append("updated_at = ?")
        params.extend([current_time, log_id, entry_id])
        
        query = f"""
            UPDATE fishing_log_entries 
            SET {', '.join(update_fields)}
            WHERE fishing_log_id = ? AND id = ?
        """
        
        cursor.execute(query, params)
        conn.commit()
        
        if cursor.rowcount == 0:
            return None
        return True

def delete_fishing_log_entry(log_id, entry_id):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM fishing_log_entries 
            WHERE fishing_log_id = ? AND id = ?
        """, (log_id, entry_id))
        conn.commit()
        return cursor.rowcount > 0

def fishing_trip_exists(trip_id):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM fishing_trips WHERE id = ?", (trip_id,))
        return cursor.fetchone() is not None