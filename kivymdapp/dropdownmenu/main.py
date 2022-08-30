from kivymd.app import MDApp
from kivymd.uix.floatlayout import  MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu


class Root(MDFloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.menu_items = [
            {
                "text": f"Item {i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Item {i}": self.set_item(x),
            } for i in range(5)
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.button,
            items = self.menu_items,
            width_mult = 4,
            position="bottom",
        )


    def set_item(self,text):
        self.ids.button.text = text
        print(text)
        self.menu.dismiss()

class TestApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Dark"
        root = Root()
        return root



if __name__ == "__main__":
    TestApp().run()
