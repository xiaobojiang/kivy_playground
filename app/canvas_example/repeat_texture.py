from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, ListProperty
from kivy.lang import Builder

kv='''
<LabelOnBackground>
    canvas.before:
        Color: 
            rgb: self.background
        Rectangle:
            pos: self.pos
            size: self.size

FloatLayout:
    canvas.before:
        Color:
            rgb: 1,1,1
        Rectangle:
            pos: self.pos
            size: self.size
            texture: app.texture
    LabelOnBackground:
        text: '{} (try to resize window)'.format(root.size)
        color: (0.4,1,1,1)
        background: (0.3,0.3,0.3)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint: None, None
        height: 30
        width: 250
'''


class LabelOnBackground(Label):
    background = ListProperty((0.2,0.2,0.2))

class RepeatTexture(App):

    texture = ObjectProperty()

    def build(self):
        self.texture = Image(source='mtexture1.png').texture
        self.texture.wrap = 'mirrored_repeat'
        self.texture.uvsize = (8,8)
        return Builder.load_string(kv)

if __name__ == '__main__':
    RepeatTexture().run()