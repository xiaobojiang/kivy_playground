from kivymd.app import MDApp
from kivy.lang import Builder


class Test(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.accent_palette = "Green"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(
            '''
BoxLayout:
    orientation:'vertical'

    MDToolbar:
        title: 'Bottom navigation'
        md_bg_color: self.theme_cls.accent_color #.2, .2, .2, 1
        specific_text_color: 1, 1, 1, 1

    MDBottomNavigation:
        panel_color: .2, .2, .2, 1

        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'Python'
            icon: 'language-python'

            MDLabel:
                text: 'Python'
                halign: 'center'

        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'C++'
            icon: 'language-cpp'

            MDLabel:
                text: 'I programming of C++'
                halign: 'center'

        MDBottomNavigationItem:
            name: 'screen 3'
            text: 'JS'
            icon: 'language-javascript'

            MDLabel:
                text: 'JS'
                halign: 'center'
'''
        )


Test().run()
