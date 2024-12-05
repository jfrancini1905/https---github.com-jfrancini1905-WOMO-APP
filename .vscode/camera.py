from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.graphics import Ellipse, Color
from kivy.app import App
import os

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        # Kamera erstellen, aber noch nicht starten
        self.camera = Camera(resolution=(640, 480), size_hint=(1, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        layout.add_widget(self.camera)

        # Capture Button
        capture_button = Button(text="Foto", size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'y': 0})
        capture_button.bind(on_press=self.capture)
        layout.add_widget(capture_button)

        # Close Button, oben rechts
        close_button = Button(size_hint=(None, None), size=(50, 50),
                              background_normal='', background_color=(1, 0, 0, 1),
                              pos_hint={'right': 1, 'top': 1})
        close_button.bind(on_press=self.go_back_to_stellplatz)

        # Runder Button mit X (wir zeichnen ein X auf den Button)
        with close_button.canvas:
            self.ellipse_color = Color(1, 1, 1, 1)  # Weißes X
            self.ellipse = Ellipse(pos=close_button.pos, size=close_button.size)
            close_button.bind(pos=self.update_shape, size=self.update_shape)
        layout.add_widget(close_button)

        # Zurück-Button, unten links
        back_button = Button(text='zurück', size_hint=(None, None), size=(150, 50), pos_hint={'x': 0, 'y': 0})
        back_button.bind(on_press=self.go_back_to_stellplatz)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_enter(self):
        # Die Kamera starten, wenn der Bildschirm betreten wird
        self.start_camera()

    def on_leave(self):
        # Die Kamera stoppen, wenn der Bildschirm verlassen wird
        self.stop_camera()

    def update_shape(self, instance, value):
        # Größe und Position des X im Close-Button aktualisieren
        self.ellipse.pos = instance.pos
        self.ellipse.size = instance.size

    def start_camera(self):
        # Die Kamera starten
        self.camera.play = True
        print("Kamera gestartet")

    def stop_camera(self):
        # Die Kamera stoppen
        self.camera.play = False
        print("Kamera gestoppt")

    def capture(self, instance):
        # Foto aufnehmen und speichern
        image_path = os.path.join("Fotos", "Foto_image.png")
        self.camera.export_to_png(image_path)
        print("Foto aufgenommen und gespeichert:", image_path)

        # Bilderliste aktualisieren
        app = App.get_running_app()
        app.add_image_to_gallery(image_path)

    def go_back_to_stellplatz(self, instance):
        # Kamera stoppen
        self.stop_camera()
        
        # Bildschirm wechseln
        self.manager.current = 'stellplatz'
