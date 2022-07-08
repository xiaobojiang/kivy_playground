from kivy.lang import Builder
from kivy.factory import Factory
from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem


#how to find the icon name: https://materialdesignicons.com/

Builder.load_string(
    '''
#:import images_path kivymd.images_path


<IconExamle@Screen>

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)

        MDBoxLayout:
            adaptive_height: True

            MDIconButton:
                icon: 'ab-testing'

'''
)


class MainApp(MDApp):
    def build(self):
        return Factory.IconExamle()


MainApp().run()