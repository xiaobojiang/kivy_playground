import kivy
kivy.require('2.0.0')

from glob import glob
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock  import Clock
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty


class Picture(Scatter):
    source = StringProperty(None)


class PicturesApp(App):
    def build(self):
        root = self.root

        curdir = dirname(__file__)
        for filename in glob(join(curdir, 'images', '*')):
            try:
                picture = Picture(source=filename, rotation =randint(-30,30))
                root.add_widget(picture)
            except Exception as e:
                Logger.exception('Pictures: unable to load {}'.format(filename))

        pop = Popup(title='load success!', content=Label(text='pics in {}/images'.format(curdir)),auto_dismiss=False)
        pop.open()
        Clock.schedule_once(pop.dismiss, 1)

    def on_pause(self):
        return True

if __name__ == '__main__':
    PicturesApp().run()