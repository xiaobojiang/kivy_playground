from kivy.app import App
from kivy.lang import Builder

kv='''
FloatLayout:
    Button:
        text: 'hello world'
        size_hint: None, None
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        canvas.before:
            PushMatrix
            Rotate:
                angle: 45
                origin: self.center
        canvas.after:
            PopMatrix
            
'''


class RotationApp(App):
    def build(self):
        return Builder.load_string(kv)

if __name__ == '__main__':
    RotationApp().run()