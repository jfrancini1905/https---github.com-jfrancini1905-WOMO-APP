import kivy
kivy.require('1.11.0')

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
from kivy.uix.camera import Camera  # Importieren Sie das Camera-Widget
from kivy.graphics import Color, Ellipse

from plyer import gps
import os
from datetime import datetime

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
        self.ids.GPS_Koordinaten.text = f"Breite: {latitude}, Länge: {longitude}"
        gps.stop()  

    def get_current_location(self, *args):
        try:
            # GPS-Daten abrufen
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            gps.start()
            self.ids.GPS_Koordinaten.text = "GPS wird abgerufen..."
        except NotImplementedError:
            self.ids.GPS_Koordinaten.text = "GPS wird auf diesem Gerät nicht unterstützt."

    def on_status(self, stype, status):
        # Statusmeldung (z. B. Fehler oder Erfolg)
        if stype == "provider-enabled":
             self.ids.GPS_Koordinaten.text = "GPS aktiviert."
        elif stype == "provider-disabled":
             self.ids.GPS_Koordinaten.text = "GPS deaktiviert."

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
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Kamera-Widget
        self.camera = Camera(resolution=(640, 480), size_hint=(1, 0.8))
        layout.add_widget(self.camera)

        # Button zum Aufnehmen eines Fotos
        self.capture_button = Button(text="Foto aufnehmen", size_hint=(1, 0.2))
        self.capture_button.bind(on_press=self.capture)
        layout.add_widget(self.capture_button)

        # Runder Button mit einem X, oben rechts platziert
        close_button = Button(size_hint=(None, None), size=(50, 50),
                              background_normal='', background_color=(1, 0, 0, 1),
                              pos_hint={'right': 1, 'top': 1})
        close_button.bind(on_press=self.go_back_to_stellplatz)
        with close_button.canvas:
            self.ellipse_color = Color(1, 1, 1, 1)
            self.ellipse = Ellipse(pos=close_button.pos, size=close_button.size)
            close_button.bind(pos=self.update_shape, size=self.update_shape)
        layout.add_widget(close_button)

        self.add_widget(layout)

    def on_enter(self):
        self.start_camera()

    def update_shape(self, instance, value):
        self.ellipse.pos = instance.pos
        self.ellipse.size = instance.size

    def start_camera(self):
        # Die Kamera starten
        self.camera.play = True

    def capture(self, instance):
        # Bild speichern
        file_path = os.path.join(App.get_running_app().user_data_dir, f"IMG_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        self.camera.export_to_png(file_path)

        # Galerie aktualisieren
        self.manager.get_screen('gallery').update_gallery()

        # Wechsel zur Galerie
        self.manager.current = 'gallery'

    def go_back_to_stellplatz(self, instance):
        self.manager.current = 'stellplatz'

class ImageGalleryScreen(Screen):
    def __init__(self, **kwargs):
        super(ImageGalleryScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.scroll_view = ScrollView()
        self.grid_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))

        self.scroll_view.add_widget(self.grid_layout)
        layout.add_widget(self.scroll_view)

        self.add_widget(layout)

    def on_enter(self):
        self.update_gallery()

    def update_gallery(self):
        # Lösche vorhandene Widgets
        self.grid_layout.clear_widgets()

        # Lade die Bilder neu
        image_dir = App.get_running_app().user_data_dir
        for filename in os.listdir(image_dir):
            if filename.endswith('.png'):
                image_path = os.path.join(image_dir, filename)
                img = Image(source=image_path, size_hint_y=None, height=200)
                self.grid_layout.add_widget(img)

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
        sm.add_widget(ImageGalleryScreen(name='gallery'))  # Hinzufügen der Galerie

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

    def add_more_options(self, label_text, checkbox_list, popup):
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
        new_option.add_widget(new_label)
        new_option.add_widget(new_checkbox)
        checkbox_list.add_widget(new_option)
        popup.dismiss()

    def get_checkbox_states(self, checkbox_list):
        states = {}
        for item in checkbox_list.children:
            if isinstance(item, BoxLayout):
                label = item.children[0]     # Label ist das erste Kind im Layout
                checkbox = item.children[1]  # Checkbox ist das zweite Kind im Layout
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
