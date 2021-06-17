# import os
# os.environ['KIVY_TEXT'] = 'pil'
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

Builder.load_string('''
<GridLayout>
    canvas.before:
        BorderImage:
            border: 10,10,10,10
            source: './button_white.png'
            pos: self.pos
            size: self.size

<RootWidget>
    GridLayout:
        size_hint: 0.9,0.9
        pos_hint: {'center_x':0.5,'center_y':0.5}
        rows:1
        Label:
            text: "Line 1"
            text_size: self.width-20, self.height-20
            valign: 'top'
        Label:
            text: "Line 2"
            text_size: self.width-20, self.height-20
            valign: 'middle'
            halign: 'center'
        Label:
            text: "Line 3LOOOOOOOOOOOOOOOOOOOOOOOOONG"
            text_size: self.width-50, self.height-10
            valign: 'bottom'
            halign: 'justify'
        
''')

class RootWidget(FloatLayout):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()



if __name__ == '__main__':
    MainApp().run()