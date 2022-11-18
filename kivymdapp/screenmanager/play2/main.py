"""Connect to "KivyBLETest" server and test various BLE functions
"""
import time

from kivymd.app import MDApp
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.properties import BooleanProperty, StringProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex

import string
from kivymd.uix.textfield import MDTextField
import json

Config.set('kivy', 'log_level', 'debug')
Config.set('kivy', 'log_enable', '1')


class MainWid(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.EntryLayout = EntryLayout()
        self.ManualLayout = None
        self.MainLayout  = None
        self.mainwid = Screen(name='MainLayout')
        self.mainwid.add_widget(self.EntryLayout)
        self.add_widget(self.mainwid)
    def switch_screen(self, mainconfirmed, tuneconfirmed=False):
        if mainconfirmed:
            if tuneconfirmed:
                self.ManualLayout = ManualLayout()
                if self.MainLayout:
                    self.mainwid.remove_widget(self.MainLayout)
                    self.MainLayout = None
                if self.EntryLayout:
                    self.mainwid.remove_widget(self.EntryLayout)
                    self.EntryLayout = None
                self.mainwid.add_widget(self.ManualLayout)
                
            else:
                self.MainLayout = MainLayout()
                if self.EntryLayout:
                    self.mainwid.remove_widget(self.EntryLayout)
                    self.EntryLayout = None
                if self.ManualLayout:
                    self.mainwid.remove_widget(self.ManualLayout)
                    self.ManualLayout = None
                self.mainwid.add_widget(self.MainLayout)
        else:
            self.EntryLayout = EntryLayout()
            if self.MainLayout:
                self.mainwid.remove_widget(self.MainLayout)
                self.MainLayout = None
            if self.ManualLayout:
                self.mainwid.remove_widget(self.ManualLayout)
                self.ManualLayout = None
            self.mainwid.add_widget(self.EntryLayout)
            


class EntryLayout(BoxLayout):
    pass
class MainLayout(BoxLayout):
    scene_label_id = ObjectProperty(None)
    pass
class ManualLayout(BoxLayout):
    pass

class NumberTextInput(MDTextField):
    def __init__(self, **kwargs):
        super(NumberTextInput, self).__init__(**kwargs)
        self.input_filter = 'int'
        self.do_wrap = False
        self.font_size = "16sp"
        self.halign = 'left'

    def insert_text(self, substring, from_undo=False):
        if substring in string.digits:
            cc, cr = self.cursor
            text = self._lines[cr]
            new_text = text[:cc] + substring + text[cc:]
            if int(new_text) > 100:
                #new input which makes input > 100 will removed
                return
            super(NumberTextInput, self).insert_text(substring, from_undo=from_undo)
        else:
            pass

class BLETestApp(MDApp):
    state = StringProperty('new')
    test_string = StringProperty('')
    rssi = StringProperty('')
    notification_value = StringProperty('')
    counter_value = StringProperty('')
    increment_count_value = StringProperty('')
    incremental_interval = StringProperty('100')
    counter_max = StringProperty('128')
    counter_value = StringProperty('')
    counter_state = StringProperty('')
    counter_total_time = StringProperty('')
    queue_timeout_enabled = BooleanProperty(True)
    queue_timeout = StringProperty('1000')
    device_name = StringProperty('MyESP32')
    device_address = StringProperty('')
    console_text = StringProperty('')
    store = JsonStore('bletestapp.json')
    dim_level = NumericProperty(100)
    cct = NumericProperty(6500)
    MAX_CCT_VALUE = NumericProperty(6500)
    MIN_CCT_VALUE = NumericProperty(2700)
    STEP_CCT_VALUE = NumericProperty(100)
    x = False
    current_scene = StringProperty('')
    setting_dict = {}
    setting_dict['hcct'] = 0
    setting_dict['lcct'] = 0
    setting_dict['uv'] = 0
    setting_dict['sup'] = 0
    setting_text = StringProperty(json.dumps(setting_dict))

    device_list = []

    uids = {
        'string': 'beb5483e-36e1-4688-b7f5-ea07361b26a8', #characteristics
        'counter_reset': '0d02',
        'counter_increment': '0d03',
        'counter_read': '0d04',
        'notifications': '0d05'
    }

    def build(self):
        if self.store.exists('device'):
            self.device_address = self.store.get('device')['address']
        else:
            self.device_address = ''
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.accent_hue = "600"
        self.mainwid = MainWid()
        return self.mainwid

    def slider_value_change(self, slider_key, slider_value):
        if str(slider_key) in self.setting_dict:
            self.setting_dict[slider_key] = slider_value
            self.setting_text = json.dumps(self.setting_dict)
        #pass

    def switch_app_screen(self,dt):
        self.mainwid.switch_screen(True)
        self.current_scene = "test"

    def switch_entry_screen(self,dt):
        self.mainwid.switch_screen(False)
    
    def toolbar_callback(self, pagename):
        if pagename is "tune":
            self.mainwid.switch_screen(True, tuneconfirmed=True)

        if pagename is "home":
            self.mainwid.switch_screen(True, tuneconfirmed=False)

    def start_scan(self):
        if self.x==False:
            self.x=True
            #time.sleep(2)
            Clock.schedule_once(self.switch_app_screen,2)
            #self.switch_app_screen(True)
        else:
            self.x=False
            #time.sleep(2)
            #self.switch_app_screen(False)
            Clock.schedule_once(self.switch_entry_screen,2)
    
    def update_cct(self, cct):
        print(f"cct changes to {cct}")

    def update_dimlevel(self, level):
        print(f"light changes to {level}")
    
    def change_scene(self, scene_no):
        print(f'scene changes to {scene_no}')
        if scene_no == 1:
            self.cct = 50
            self.dim_level = 30
        elif scene_no == 2:
            self.cct = 80
            self.dim_level = 100



if __name__ == '__main__':
    BLETestApp().run()
