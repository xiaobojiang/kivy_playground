# import os
# os.environ['KIVY_TEXT'] = 'pil'
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.lang import Builder

Builder.load_string('''
<GridLayout>
    canvas.before:
        BorderImage:
            border: 10,10,10,10
            texture: self.background_image.texture
            pos: self.pos
            size: self.size

<RootWidget>
    CustomLayout:
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

class CustomLayout(GridLayout):
    background_image = ObjectProperty(
        Image(
            source='./button_white_animated.zip',
            anim_delay=0.1
        )
    )

class RootWidget(FloatLayout):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()



if __name__ == '__main__':
    MainApp().run()