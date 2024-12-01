import sqlite3


def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

# Tabelle erstellen
def create_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        location TEXT NOT NULL,
        checklist Text NOT NULL,
        picture BLOB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn.execute(query)
    conn.commit()

# Eintrag hinzufügen
def add_entry(conn, title, location, checklist):
    query = "INSERT INTO entries (title, location, checklist) VALUES (?, ?, ?);"
    conn.execute(query, (title, location, checklist))
    conn.commit()

   

def get_entry_by_id(conn, entry_id):
    query = f"SELECT * FROM entries WHERE id = {entry_id};"
    cursor = conn.execute(query)
    return cursor.fetchone()

# Alle Einträge abrufen
def get_all_entries(conn):
    query = "SELECT * FROM entries;"
    cursor = conn.execute(query)
    return cursor.fetchall()

def get_entry_by_title(conn, title):
    query = f"SELECT * FROM entries WHERE title = {title};"
    cursor = conn.execute(query)
    return cursor.fetchone()


# Eintrag aktualisieren
def update_entry(conn, entry_id, title, description):
    query = f"UPDATE entries SET title = {title}, description = {description}, TIMESTAMP = CURRENT_TIMESTAMP WHERE id = {entry_id};"
    conn.execute(query, (title, description, entry_id))
    conn.commit()
  

# Eintrag löschen
def delete_entry(conn, entry_id):
    query = f"DELETE FROM entries WHERE id = {entry_id};"
    conn.execute(query, (entry_id,))
    conn.commit()
    
    
#Verbindung schliessen
def close_connection(conn):
    conn.close()
    

