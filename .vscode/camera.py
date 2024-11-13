from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.camera = Camera(play=True, resolution=(640, 480))
        layout.add_widget(self.camera)

        capture_button = Button(text="Capture", size_hint=(1, 0.2))
        capture_button.bind(on_press=self.capture)
        layout.add_widget(capture_button)

        self.add_widget(layout)

    def capture(self, instance):
        self.camera.export_to_png("captured_image.png")
        print("Captured Image")
