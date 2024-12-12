import sqlite3

DB_INSTANCE = 'instance/database.db'

def create_tables():
    conn = sqlite3.connect(DB_INSTANCE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lastName TEXT NOT NULL,
                    firstName INTEGER NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def add_user(lastName, firstName, email, password):
    conn = sqlite3.connect(DB_INSTANCE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (lastName, firstName, email, password) VALUES (?, ?, ?, ?)", 
                   (lastName, firstName, email, password))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect(DB_INSTANCE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users