from typing import List
from kivy.app import App
from kivy.properties import OptionProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from math import cos, sin


class LinePlayground(FloatLayout):
    alpha_controlline = NumericProperty(1.0)
    alpha = NumericProperty(0.5)
    close = BooleanProperty(False)
    points = ListProperty([(500, 500),
                          [300, 300, 500, 300],
                          [500, 400, 600, 400]])
    points2 = ListProperty([])
    joint = OptionProperty('none', options=('round','miter','bevel','none'))
    cap = OptionProperty('none', options=('round','square','none'))
    linewidth = NumericProperty(10.0)
    dt = NumericProperty(0)
    dash_length = NumericProperty(1)
    dash_offset = NumericProperty(0)
    dashes = ListProperty([])

    _update_points_animation_ev = None

    def on_touch_down(self, touch):
        if super(LinePlayground, self).on_touch_down(touch):
            return True
        touch.grab(self)
        self.points.append(touch.pos) #add point at the tail
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.points[-1] = touch.pos #update tail point
            return True
        return super(LinePlayground, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True
        return super(LinePlayground, self).on_touch_up(touch)

    def animate(self, do_animation):
        if do_animation:
            self._update_points_animation_ev = Clock.schedule_interval(
                self.update_points_animation, 0
            )
        elif self._update_points_animation_ev is not None:
            self._update_points_animation_ev.cancel()
    
    def update_points_animation(self, dt=0):
        cy = self.height * 0.6
        cx = self.width * 0.1
        w = self.width * 0.8
        step = 20
        points = []
        points2 = []
        self.dt += dt

        for i in range(int (w/step)):
            x = i * step
            points.append(cx + x)
            points.append(cy + cos(x/w * 8. + self.dt) * self.height* 0.2)
            points2.append(cx + x)
            points2.append(cy + sin(x/w * 8. + self.dt) * self.height * 0.2)
        self.points = points
        self.points2 = points2

class TestLineApp(App):
    def build(self):
        return LinePlayground()

if __name__ == '__main__':
    TestLineApp().run()
