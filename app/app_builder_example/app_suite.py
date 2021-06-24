import sys
import re
from random import choice

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder

from kivy.uix.floatlayout import FloatLayout

print('** In main program, done with imports')

class TestBuildApp(App):
    #from build method
    def build(self):
        print('** inside build()')
        return Button(text='hello from TestBuildApp')

class TestKVFileApp(App):
    #use name, aka 'testkvfile.kv' to search kv file
    pass

class TestKVDirApp(App):
    #set the dir for searching kv file, file name shall be 'testkvdir.kv' in kv_directory aka 'app_suite_data'
    kv_directory = 'app_suite_data'

class TestKVStringApp(App):
    #from kv string 
    def build(self):
        print('** inside build()')
        widget = Builder.load_string(
            "Button:\n  text: 'hello from TestKVStringApp'"
        )
        print('** widget built')
        return widget

class TestPrebuiltApp(App):
    #use builder to create top level widget
    kv="<Prebuilt>\n    Button:\n        text:'hello from TestPrebuildApp'"
    Builder.load_string(kv)
    print("** inside TestPrebuildApp, class initialization build <Prebuilt>")

    class Prebuilt(FloatLayout):
        pass

    def build(self):
        return self.Prebuilt()

def print_class(class_name):
    filename = sys.argv[0]
    with open(filename) as f:
        data = f.read()
        regex = "^(class "+class_name+"\\b.*?)^\\S" #check the lines with multiline and dotall, until next line start with non empty character (which goes with python pattern, start with 4 spaces)
        match = re.search(regex, data, flags=re.MULTILINE | re.DOTALL) #multiline matches every line, dotall matches even \n
        if match:
            print(match.group(1))

if __name__ == '__main__':
    dash = '-'*40

    arg = sys.argv[1][0].lower() if len(sys.argv) > 1 else "h"
    print(dash)

    if arg == 'r':
        arg = choice('bfds')

    if arg == 'b':
        print_class('TestBuildApp')
        TestBuildApp().run()
    elif arg == 'f':
        print_class('TestKVFileApp')
        TestKVFileApp().run()
    elif arg == 'd':
        print_class('TestKVDirApp')
        TestKVDirApp().run()
    elif arg == 's':
        print_class('TestKVStringApp')
        TestKVStringApp().run()
    elif arg == 'p':
        print_class('TestPrebuiltApp')
        TestPrebuiltApp().run()
    else:
        print("""
        This demo runs different application windows based on a command line argument.

        Try using one of these:
        b - Use build() method to return a widget
        d - Use a kv file from a different directory
        f - Use a kv file with the widget object
        p - Use prebuilt widget inside a layout
        s - Use a kivy language string to create the widget
        r - pick one of the options at random.

        h - show this help message.

        After closing the application window, this program will exit.
        While the run() method does return, kivy cannot run another
        application window after one has been closed.
        """)

    print(dash)