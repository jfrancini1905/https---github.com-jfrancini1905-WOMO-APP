import kivy
kivy.parse_kivy_version('1.11.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from camera import CameraScreen

import dbscript

# Test
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
    def speichern_in_db(self):
        # Speichern der Daten in der Datenbank
        entries = "entries.db"
        conn = dbscript.create_connection(entries)
        dbscript.add_entry(conn,self.ids.Bezeichnung.text,self.ids.GPS_Koordinaten.text, self.ids.checklist.text)
        

class MyApp(App):
    def build(self):
        # Standardbildschirm laden (StartScreen, MainScreen, StellplatzScreen)
        Builder.load_file("MyApp.kv")
        Builder.load_file("verwaltung.kv")  # Verwaltungskv-Datei hier laden
        Builder.load_file("checkliste.kv")  # Checklistekv-Datei hier laden
        sm = MyScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(StellplatzScreen(name='stellplatz'))
        sm.add_widget(VerwaltungsScreen(name='verwaltung'))
        sm.add_widget(StellplatzverwaltungScreen(name='Stellplatzeinträge'))
        sm.add_widget(ChecklistScreen(name='checkliste'))
        #sm.add_widget(CameraScreen(name='camera'))
        return sm
    def add_more_options(self, checkbox_list):
        new_option = BoxLayout(orientation='horizontal')
        new_checkbox = CheckBox()
        new_label = Label(text='Neue Option', font_size=24)
        new_option.add_widget(new_checkbox)
        new_option.add_widget(new_label)
        checkbox_list.add_widget(new_option)
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
