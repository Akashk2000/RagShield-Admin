import sqlite3

conn = sqlite3.connect(r'C:\\Users\\akash\\Desktop\\rag\\instance\\database.db')
c = conn.cursor()

# Add new columns for admin resolution proof if they don't exist
try:
    c.execute("ALTER TABLE incident ADD COLUMN admin_comment TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists

try:
    c.execute("ALTER TABLE incident ADD COLUMN resolved_by TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists

try:
    c.execute("ALTER TABLE incident ADD COLUMN resolved_at DATETIME")
except sqlite3.OperationalError:
    pass  # Column already exists

conn.commit()
conn.close()
