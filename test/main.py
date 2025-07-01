from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window

class CameraApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1) # Set window background to white
        layout = FloatLayout()
        self.camera = Camera(play=True, index=0, resolution=(640, 480))
        layout.add_widget(self.camera)
        return layout

if __name__ == '__main__':
    CameraApp().run()