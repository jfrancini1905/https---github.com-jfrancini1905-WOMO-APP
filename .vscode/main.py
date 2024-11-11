from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

class StartScreen(Screen):
    def on_enter(self):
        # Wechsel nach 3 Sekunden zur MainScreen
        Clock.schedule_once(self.switch_to_main, 1)

    def switch_to_main(self, dt):
        self.manager.current = 'main'

#test

class MainScreen(Screen):
    pass

class StellplatzScreen(Screen):
    pass

class VerwaltungsScreen(Screen):
    pass

class StellplatzverwaltungScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(StellplatzScreen(name='stellplatz'))
        sm.add_widget(VerwaltungsScreen(name='verwaltung'))
        sm.add_widget(StellplatzverwaltungScreen(name='Stellplatzeinträge'))
        return sm

if __name__ == "__main__":
    MyApp().run()
    
class verwaltung(App):
        def build(self):
            sm = MyScreenManager()
            sm.add_widget(VerwaltungsScreen(name='verwaltung'))
            sm.add_widget(StellplatzverwaltungScreen(name='Stellplatzeinträge'))
            return sm
        
if __name__ == "verwaltung":
    verwaltung().run()
