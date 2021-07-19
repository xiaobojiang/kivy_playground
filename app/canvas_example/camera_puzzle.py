from ctypes import alignment
from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.slider import Slider
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty
from random import random, randint
from functools import partial

class Puzzle(Camera):
    blocksize = NumericProperty(100)

    def on_texture_size(self, instance, value):
        self.build()

    def on_blocksize(self, instance, value):
        self.build()

    def build(self):
        self.clear_widgets()
        texture = self.texture
        if not texture:
            return
        bs = self.blocksize
        tw,th = self.texture_size
        for x in range(int(tw/bs)):
            for y in range(int(th/bs)):
                bx = x*bs
                by = y*bs
                subtexture = texture.get_region(bx,by,bs,bs)
                node = Scatter(pos=(bx,by), size=(bs,bs))
                with node.canvas:
                    Color(1,1,1)
                    Rectangle(size=node.size, texture=subtexture)
                self.add_widget(node)
        self.shuffle()

    def shuffle(self):
        texture = self.texture
        bs = self.blocksize
        tw, th = self.texture_size
        count = int(tw/bs)*int(th/bs)
        indices = list(range(count))
        childindex = 0
        while indices:
            index = indices.pop(randint(0,len(indices)-1))
            x = bs * (index%(int(tw/bs))) + self.parent.center_x - 0.5*bs*(tw//bs) #make it in center
            y = bs * int(index/int(tw/bs)) + self.parent.center_y - 0.5*bs*(th//bs)
            child = self.children[childindex] #get the child widget (Scatter)
            a = Animation(d=random()/4.) + Animation(pos=self.to_parent(x,y, relative=True), t= 'out_quad', d=0.4)
            a.start(child)
            childindex += 1
    
    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.shuffle()
            return True
        super(Puzzle, self).on_touch_down(touch)

    
class PuzzleApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        wid = Widget()
        puzzle = Puzzle(resolution=(640,480), play=True)
        puzzle.size_hint_y = None
        puzzle.height = '0dp' #make the camera widget invisible (the gened scatter still there)
        slider = Slider(min=100,max=200,step=10,size_hint=(1.0, 0.1))
        slider.bind(value=partial(self.on_value, puzzle))
        wid.add_widget(puzzle)

        root.add_widget(wid)
        root.add_widget(slider)
        return root

    def on_value(self, puzzle, instance, value):
        value = int((value+5)/10)*10
        puzzle.blocksize = value
        instance.value = value

if __name__ == '__main__':
    PuzzleApp().run()
        


                

    