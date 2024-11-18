import kivy
kivy.parse_kivy_version('1.11.0')
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

# Importiere die CameraScreen-Klasse, falls vorhanden
from camera import CameraScreen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox

import dbscript

# Definiere die Screens
class StartScreen(Screen):
    def on_enter(self):
        # Wechsel nach 2 Sekunden zur MainScreen
        Clock.schedule_once(self.switch_to_main, 2)

    def switch_to_main(self, dt):
        self.manager.current = 'main'

class MainScreen(Screen):
    pass

class StellplatzScreen(Screen):
    pass

class ChecklistScreen(Screen):
    pass

class VerwaltungsScreen(Screen):
    pass

class StellplatzverwaltungScreen(Screen):
    pass

class CameraScreen(Screen):
    pass

# Der ScreenManager, der die Screens verwaltet
class MyScreenManager(ScreenManager):
    pass

class MyRootWidget(BoxLayout):
    def speichern_in_db(self, checkbox_list):
        # Speichern der Daten in der Datenbank
        get_checkbox_states = self.get_checkbox_states(checkbox_list)
        entries = "entries.db"
        conn = dbscript.create_connection(entries)
        dbscript.add_entry(conn, self.ids.Bezeichnung.text, self.ids.GPS_Koordinaten.text, self.ids.checklist.text)

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
        # Standardbildschirm laden (StartScreen, MainScreen, StellplatzScreen)
        Builder.load_file("MyApp.kv")
        Builder.load_file("verwaltung.kv")  
        Builder.load_file("checkliste.kv")  
        sm = MyScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(StellplatzScreen(name='stellplatz'))
        sm.add_widget(VerwaltungsScreen(name='verwaltung'))
        sm.add_widget(StellplatzverwaltungScreen(name='Stellplatzeinträge'))
        sm.add_widget(ChecklistScreen(name='checkliste'))
        sm.add_widget(CameraScreen(name='camera'))
        return sm

    def show_popup(self, checkbox_list):
        # Layout für das Popup
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # TextInput für die Eingabe
        text_input = TextInput(hint_text="Gib den Text für das Label ein", size_hint_y=None, height=50)

        # Button zum Hinzufügen
        confirm_button = Button(
            text="Hinzufügen",
            size_hint_y=None,
            height=50,
            on_release=lambda btn: self.add_more_options(checkbox_list, text_input.text, popup)
        )

        # Elemente zum Popup-Layout hinzufügen
        popup_layout.add_widget(Label(text="Gib einen Text ein:"))
        popup_layout.add_widget(text_input)
        popup_layout.add_widget(confirm_button)

        # Popup erstellen
        popup = Popup(
            title="Neue Option hinzufügen",
            content=popup_layout,
            size_hint=(0.8, 0.4),  
            auto_dismiss=False  
        )

        # Popup anzeigen
        popup.open()

    def add_more_options(self, checkbox_list, label_text, popup):
        # Text prüfen
        if not label_text.strip():
            label_text = f"Option {len(checkbox_list.children) + 1}"

        # Neues BoxLayout erstellen
        new_option = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=50,
            spacing=10
        )

        # Checkbox und Label hinzufügen
        new_checkbox = CheckBox()
        new_label = Label(text=label_text, font_size=24)

        new_option.add_widget(new_checkbox)
        new_option.add_widget(new_label)

        # Neues Element zur Liste hinzufügen
        checkbox_list.add_widget(new_option)

        # Popup schließen
        popup.dismiss()
    def get_checkbox_states(self, checkbox_list):
        states = {}
        for item in checkbox_list.children:
            if isinstance(item, BoxLayout):
                checkbox = item.children[1]  # Checkbox ist das zweite Kind im Layout
                label = item.children[0]     # Label ist das erste Kind im Layout
                if isinstance(checkbox, CheckBox) and isinstance(label, Label):
                    states[label.text] = checkbox.active  # True oder False für aktiv/inaktiv
        return states

if __name__ == '__main__':
    app = MyApp()
    app.run()
