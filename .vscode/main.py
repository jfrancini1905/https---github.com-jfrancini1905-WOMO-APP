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
        conn = dbscript.create_connection(entries.db)
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
        sm.add_widget(CameraScreen(name='camera'))
        return sm

if __name__ == '__main__':
    app = MyApp()
    app.run()
