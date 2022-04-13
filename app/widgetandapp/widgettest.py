from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout

class MainLayout(BoxLayout):
    #device_text = StringProperty()
    pass


class WidgetTestApp(App):
    devices = StringProperty()
    def update_devices(self, dt):
        #option 1 to update text in widget
        self.devices += f"device {dt}\n"
        #print(self.ids)
        #option 2 to update text in widget
        self.root.ids.device_text.text += f"{dt}..."
    def build(self):
        root = MainLayout()
        Clock.schedule_interval(self.update_devices, 1.0)
        return root


if __name__ == '__main__':
    WidgetTestApp().run()