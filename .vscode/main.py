import kivy
kivy.parse_kivy_version('1.11.0')
import plyer
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
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.layout import Layout
from kivy.uix.image import Image
from camera import CameraScreen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox

import dbscript

# Definieren der Screens
class StartScreen(Screen):
    def on_enter(self):
        # Wechsel nach 2 Sekunden zum Main-Screen
        Clock.schedule_once(self.switch_to_main, 2)

    def switch_to_main(self, dt):
        self.manager.current = 'main'

class MainScreen(Screen):
    pass

class StellplatzScreen(Screen):
    def on_location(self, **kwargs):
        # Standortdaten verarbeiten und anzeigen
        latitude = kwargs.get('lat', 'Unbekannt')
        longitude = kwargs.get('lon', 'Unbekannt')
        self.root.ids.GPS_Koordinaten.text = f"Breite: {latitude}, Länge: {longitude}"
        gps.stop()  
    def get_current_location(self, *args):
        try:
            # GPS-Daten abrufen
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            gps.start()
            self.ids.get('GPS_Koordinaten', None).text = "GPS wird abgerufen..."
        except NotImplementedError:
            self.ids.get('GPS_Koordinaten', None).text = "GPS wird auf diesem Gerät nicht unterstützt."

    def on_status(self, stype, status):
        # Statusmeldung (z. B. Fehler oder Erfolg)
        if stype == "provider-enabled":
             self.ids.get('GPS_Koordinaten', None).text = "GPS aktiviert."
        elif stype == "provider-disabled":
             self.ids.get('GPS_Koordinaten', None).text = "GPS deaktiviert."
    def speichern_in_db(self, checkbox_list):
        try:
            checkbox_states = app.get_checkbox_states(checkbox_list)
            bezeichnung = self.ids.Bezeichnung.text.strip()
            gps_koordinaten = self.ids.GPS_Koordinaten.text.strip()     
            entries = "entries.db"
            conn = dbscript.create_connection(entries)

            if conn:
                dbscript.add_entry(conn, bezeichnung, gps_koordinaten, checkbox_states)
                app.show_success_popup()  # Popup anzeigen
            else:   
                app.show_error_popup("Fehler bei Verbindung mit der Datenbank")
                
        except Exception as e:
            app.show_error_popup("Fehler beim Speichern: " + str(e))
        finally:
            if conn:
                conn.close()

    

class ChecklistScreen(Screen):
    pass

class VerwaltungsScreen(Screen):
    pass

class StellplatzverwaltungScreen(Screen):
    pass

class StellplatzübersichtScreen(Screen):
    pass

class CameraScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass

class CustomScrollView(ScrollView):
    def __init__(self, **kwargs):
        super(CustomScrollView, self).__init__(**kwargs)
        self.container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.container.bind(minimum_height=self.container.setter('height'))
        super(CustomScrollView, self).add_widget(self.container)

    def add_widget(self, widget, *args, **kwargs):
        self.container.add_widget(widget, *args, **kwargs)
        self._trigger_update_from_scroll()

    def remove_widget(self, widget, *args, **kwargs):
        self.container.remove_widget(widget, *args, **kwargs)
        self._trigger_update_from_scroll()

class MyApp(App):
    def build(self):
        # Standardbildschirme laden
        Builder.load_file("MyApp.kv")
        Builder.load_file("verwaltung.kv")  
        Builder.load_file("checkliste.kv") 
        Builder.load_file("uebersicht.kv") 
        sm = MyScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(StellplatzScreen(name='stellplatz'))
        sm.add_widget(VerwaltungsScreen(name='verwaltung'))
        sm.add_widget(StellplatzverwaltungScreen(name='Stellplatzeinträge'))
        sm.add_widget(ChecklistScreen(name='checkliste'))
        sm.add_widget(StellplatzübersichtScreen(name='uebersicht'))
        sm.add_widget(CameraScreen(name='camera'))
        return sm

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

    def add_more_options(self, checkbox_list, label_text, popup):
        if not label_text.strip():
            label_text = f"Option {len(checkbox_list.children) + 1}"

        new_option = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=50,
            spacing=10
        )
        # Checkbox und Label hinzufügen
        new_label = Label(text=label_text, font_size=32, color=(0, 0, 0, 1)) #Schwarze Textfarbe 
        new_checkbox = CheckBox()
        new_label = Label(text=label_text, font_size=24)
        new_option.add_widget(new_checkbox)
        new_option.add_widget(new_label)
        checkbox_list.add_widget(new_option)
        popup.dismiss()
    def get_checkbox_states(self, checkbox_list):
        states = {}
        for item in checkbox_list.children:
            if isinstance(item, BoxLayout):
                checkbox = item.children[0]  # Checkbox ist das zweite Kind im Layout
                label = item.children[1]     # Label ist das erste Kind im Layout
                if isinstance(checkbox, CheckBox) and isinstance(label, Label):
                    states[label.text] = checkbox.active
        return states
    
    def show_success_popup(self):
        # Popup-Inhalt
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        message = Label(text="Daten wurden erfolgreich gespeichert!", halign='center')
        content.add_widget(message)

        close_button = Button(text="OK", size_hint=(1, 0.5))
        content.add_widget(close_button)

        popup = Popup(
            title="Erfolg",
            content=content,
            size_hint=(0.7, 0.4),  
            auto_dismiss=False 
        )
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def show_error_popup(self, error_message="Ein Fehler ist aufgetreten."):
        # Layout für den Popup-Inhalt
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        message = Label(text=f"[b]Fehler:[/b] {error_message}", markup=True, halign='center')
        content.add_widget(message)

        close_button = Button(text="OK", size_hint=(1, 0.5))
        content.add_widget(close_button)

        popup = Popup(
            title="Speichern fehlgeschlagen",
            content=content,
            size_hint=(0.7, 0.4), 
            auto_dismiss=False 
        )

        close_button.bind(on_release=popup.dismiss)

        popup.open()

if __name__ == '__main__':
    app = MyApp()
    app.run()
