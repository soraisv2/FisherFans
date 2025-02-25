import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()

db_instance = os.getenv("DB_INSTANCE")

if not db_instance:
    raise ValueError("DB_INSTANCE is not configured in the .env file")

def add_fishing_log(title, description, user_id):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fishing_logs (title, description, user_id) 
            VALUES (?, ?, ?)
        """, (title, description, user_id))
        conn.commit()
        
        log_id = cursor.lastrowid
        
    return {
        "id": log_id,
        "title": title,
        "description": description,
        "user_id": user_id
    }


def get_fishing_logs(filters=None):
    with sqlite3.connect(db_instance) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = """
            SELECT id, title, description, created_at, user_id 
            FROM fishing_logs
        """
        params = []

        if filters:
            conditions = []
            if "user_id" in filters:
                conditions.append("user_id = ?")
                params.append(filters["user_id"])
            if "title" in filters:
                conditions.append("title LIKE ?")
                params.append(f"%{filters['title']}%")
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, params)
        logs = cursor.fetchall()

        return [
            {
                "id": log["id"],
                "title": log["title"],
                "description": log["description"],
                "created_at": log["created_at"],
                "user_id": log["user_id"]
            }
            for log in logs
        ]

def get_fishing_log(log_id):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fishing_logs WHERE id = ?", (log_id,))
        log = cursor.fetchone()
    return log

def modify_fishing_log(log_id, title, description):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE fishing_logs 
            SET title = ?, description = ?
            WHERE id = ?
        """, (title, description, log_id))
        conn.commit()

def delete_fishing_log(log_id):
    with sqlite3.connect(db_instance) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fishing_logs WHERE id = ?", (log_id,))
        conn.commit()