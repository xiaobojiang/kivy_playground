from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Goto settings'
            on_press: root.manager.current = 'settings'
        Button:
            text: 'Quit'

<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
        #Camera:
        #    resolution: (480,320)
        Label:
            text: app.slogan_app
        Label:
            text: root.slogan
""")



# Declare both screens
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    slogan = StringProperty('testing')
    pass
    # slogan_id = ObjectProperty()
    #
    # def __init__(self, *args, **kwargs):

    #     self.slogan_id.text = 'work hard, play hard'

class TestApp(App):
    slogan_app = StringProperty('testingapp')
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm

if __name__ == '__main__':
    TestApp().run()