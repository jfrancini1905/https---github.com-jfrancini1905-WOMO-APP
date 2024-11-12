from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

# Test
# Definiere die Screens
class StartScreen(Screen):
    def on_enter(self):
        # Wechsel nach 3 Sekunden zur MainScreen
        Clock.schedule_once(self.switch_to_main, 1)

    def switch_to_main(self, dt):
        self.manager.current = 'main'
class MainScreen(Screen):
    pass

class StellplatzScreen(Screen):
    pass

class VerwaltungsScreen(Screen):
    pass

class StellplatzverwaltungScreen(Screen):
    pass

# Der ScreenManager, der die Screens verwaltet
class MyScreenManager(ScreenManager):
    pass

class MyRootWidget(BoxLayout):
    # Diese Methode wird über on_press aufgerufen
    def speichern_in_db(self):
        print("Button wurde gedrückt!")
class MyApp(App):
    def build(self):
        # Standardbildschirm laden (StartScreen, MainScreen, StellplatzScreen)
        sm = MyScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(StellplatzScreen(name='stellplatz'))
        return sm

    def verwaltung(self):
        # Verwaltungsbildschirm und Stellplatzverwaltung laden
        Builder.load_file("verwaltung.kv")
        sm = MyScreenManager()
        sm.add_widget(VerwaltungsScreen(name='verwaltung'))
        sm.add_widget(StellplatzverwaltungScreen(name='Stellplatzeinträge'))
        return sm

if __name__ == '__main__':
    MyApp().run()
