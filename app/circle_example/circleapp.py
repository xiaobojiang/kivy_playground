from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class window(BoxLayout):
    e1 = ObjectProperty(None)
    e2 = ObjectProperty(None)
    hm = ObjectProperty(None)
    wm = ObjectProperty(None)
    

class CircleApp(App):
    def build(self):
        return window()

if __name__ == '__main__':
    CircleApp().run()