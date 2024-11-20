from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Ellipse, Color

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        # Kamera erstellen, aber nicht starten
        self.camera = Camera(resolution=(640, 480), size_hint=(1, 0.8), pos_hint={'x': 0, 'y': 0.2})
        layout.add_widget(self.camera)

        # Capture Button
        capture_button = Button(text="Foto", size_hint=(1, 0.2), pos_hint={'x': 0, 'y': 0})
        capture_button.bind(on_press=self.capture)
        layout.add_widget(capture_button)

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
        self.start_camera(self)

    def update_shape(self, instance, value):
        self.ellipse.pos = instance.pos
        self.ellipse.size = instance.size

    def start_camera(self, instance):
        # Die Kamera starten
        self.camera.play = True
        print("Kamera gestartet")

    def capture(self, instance):
        self.camera.export_to_png("Foto_image.png")
        print("Foto Image")

    def go_back_to_stellplatz(self, instance):
        self.manager.current = 'stellplatz'
