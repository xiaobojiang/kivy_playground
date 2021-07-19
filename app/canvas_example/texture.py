from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.clock import Clock


class TextureAccessibleWidget(Widget):
    texture = ObjectProperty(None)
    #https://stackoverflow.com/questions/5532595/how-do-opengl-texture-coordinates-work
    #basically, it is four coord in x,y of retangle, if more than 1, it may repeat
    tex_coords = ListProperty([0,0,1,0,1,1,0,1]) 
    texture_wrap = StringProperty('clamp_to_edge')

    def __init__(self, **kwargs):
        super(TextureAccessibleWidget, self).__init__(**kwargs)
        Clock.schedule_once(self.texture_init, 0)
    
    def texture_init(self, *args):
        self.texture = self.canvas.children[-1].texture #goes to pic

    def on_texture_wrap(self, instance, value):
        self.texture.wrap = value

class runTouchApp(App):
    def build(self):
        pass

if __name__ == '__main__':
    runTouchApp().run()