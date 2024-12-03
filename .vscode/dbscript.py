import sqlite3
import main
import kivy
kivy.parse_kivy_version('1.11.0')
import plyer
import json
from plyer import gps
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.camera import Camera  
from kivy.graphics import Color, Ellipse

from plyer import gps
import os
from datetime import datetime
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

    try:
        conn.execute(query, (title, location, checklist))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        show_error_popup("Bitte füllen sie alle Felder aus")



   

def get_entry_by_id(conn, entry_id):
    try:
        query = "SELECT * FROM entries WHERE id = ?;"
        cursor = conn.execute(query, (entry_id,))
        result = cursor.fetchone()
        return result
    except Exception as e:
        show_error_popup("Fehler beim Lesen des Eintrags")
        print(f"Error reading entry")
        return None


# Alle Einträge abrufen
def get_all_entries(conn):
    try:
        query = "SELECT * FROM entries;"
        cursor = conn.execute(query)
        return cursor.fetchall()
    except Exception as e:
        show_error_popup("Fehler beim Lesen der Einträge")
        print(f"Error retrieving entries: {e}")
        return []


def get_entry_by_title(conn, title):
    query = "SELECT * FROM entries WHERE title = ?;"
    cursor = conn.execute(query, (title,))
    return cursor.fetchone()



# Eintrag aktualisieren
def update_entry(conn, entry_id, title, description):
    query = """
    UPDATE entries 
    SET title = ?, checklist = ?, created_at = CURRENT_TIMESTAMP 
    WHERE id = ?;
    """
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
    

def show_error_popup(self, message):
        popup = Popup(title="Fehler", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

def show_popup(self, checkbox_list):
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        text_input = TextInput(hint_text="Gib den Text für das Label ein", size_hint_y=None, height=50)

        confirm_button = Button(
            text="Hinzufügen",
            size_hint_y=None,
            height=50,
            on_release=lambda btn: self.add_more_options(text_input.text, checkbox_list, popup)
        )

        # Elemente zum Popup-Layout hinzufügen
        popup_layout.add_widget(Label(text="Gib einen Text ein:"))
        popup_layout.add_widget(text_input)
        popup_layout.add_widget(confirm_button)

        popup = Popup(
            title="Neue Option hinzufügen",
            content=popup_layout,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )

        popup.open()
