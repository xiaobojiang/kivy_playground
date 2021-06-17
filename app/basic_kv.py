# import os
# os.environ['KIVY_TEXT'] = 'pil'
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.lang import Builder

root = Builder.load_string('''
FloatLayout:
    canvas.before:
        Color:
            rgba: 0,1,0,1
        Rectangle:
            pos: self.pos
            size: self.size
    Button:
        text: 'Hello World'
        size_hint: .5, .5
        pos_hint: {'center_x':0.5, 'center_y':0.5}
''')

class MainApp(App):
    def build(self):
        return root



if __name__ == '__main__':
    MainApp().run()