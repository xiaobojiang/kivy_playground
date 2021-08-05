from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder

Builder.load_string("""
<Test>
    size_hint: .5, .5
    pos_hint: {'center_x':0.5, 'center_y':0.5}
    do_default_tab: False

    TabbedPanelItem: 
        text: 'first tab'
        Label:
            text: 'first tab content area'
        
    TabbedPanelItem:
        text: 'tab2'
        BoxLayout:
            Label: 
                text: 'second tab content area'
            Button:
                text: 'Button that does nothing'
    TabbedPanelItem:
        text: 'tab3'
        RstDocument:
            text: 
                '\\n'.join(("hello world", "-----------", "you are in third tab"))
""")


class Test(TabbedPanel):
    pass

class TabbedPanelApp(App):
    def build(self):
        return Test()


if __name__ == '__main__':
    TabbedPanelApp().run()