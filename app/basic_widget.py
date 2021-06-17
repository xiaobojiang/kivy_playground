# import os
# os.environ['KIVY_TEXT'] = 'pil'
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout

class RootWidget(FloatLayout):

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

        self.add_widget(
            Button(
                text="Hello world",
                size_hint=(0.5,0.5),
                pos_hint={'center_x':0.5, 'center_y':0.5}
            )
        )

class MainApp(App):
    def build(self):
        self.root = root = RootWidget()
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            Color(0,1,0,1) #green
            self.rect = Rectangle(size=root.size, pos=root.pos)
        return root
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size



if __name__ == '__main__':
    MainApp().run()