import sqlite3

# Verbindung zur SQLite-Datenbank herstellen (erstellt die Datei, falls sie nicht existiert)
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
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn.execute(query)
    conn.commit()

# Eintrag hinzufügen
def add_entry(conn, title, description):
    query = "INSERT INTO entries (title, description) VALUES (?, ?);"
    conn.execute(query, (title, description))
    conn.commit()
    close_connection(conn)

# Alle Einträge abrufen
def get_all_entries(conn):
    query = "SELECT * FROM entries;"
    cursor = conn.execute(query)
    return cursor.fetchall()

# Eintrag aktualisieren
def update_entry(conn, entry_id, title, description):
    query = "UPDATE entries SET title = ?, description = ? WHERE id = ?;"
    conn.execute(query, (title, description, entry_id))
    conn.commit()
    close_connection(conn)

# Eintrag löschen
def delete_entry(conn, entry_id):
    query = "DELETE FROM entries WHERE id = ?;"
    conn.execute(query, (entry_id,))
    conn.commit()
    close_connection(conn)
    
#Verbindung schliessen
def close_connection(conn):
    conn.close()
    

