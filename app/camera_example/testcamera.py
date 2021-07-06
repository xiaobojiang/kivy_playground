from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import time

class CameraClick(BoxLayout):
    camera = ObjectProperty()
    def capture(self):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")

class TestCameraApp(App):
    def build(self):
        return CameraClick()


if __name__ == '__main__':
    TestCameraApp().run()