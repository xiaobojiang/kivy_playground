import kivy 
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty

class Controller(FloatLayout):
    label_wid = ObjectProperty()
    info = StringProperty()

    def do_action(self):
        self.label_wid.text = 'My label after button pressed'
        self.info = 'New info text'

# it try to find controller.kv in the same dir
class ControllerApp(App):
    def build(self):
        return Controller(info='Hello world')

if __name__ == '__main__':
    ControllerApp().run()

