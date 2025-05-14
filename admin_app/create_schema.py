import sqlite3
import os

DATABASE = r'C:\\Users\\akash\\Desktop\\rag\\instance\\database.db'

def create_schema():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create user table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        college_name TEXT NOT NULL
    )
    ''')

    # Create incident table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS incident (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES user(id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Database schema created successfully.")

if __name__ == "__main__":
    create_schema()
