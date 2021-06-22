from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup

import os
from pathlib import Path
from PyPDF3 import PdfFileMerger


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    homepath = str(Path.home())


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    homepath = str(Path.home())


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    filelist = []

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filenames):
        # with open(os.path.join(path, filename[0])) as stream:
        #     self.text_input.text = stream.read()
        self.text_input.text = 'You have selected following {} files: \n'.format(len(filenames))
        self.filelist = []
        for filename in filenames:
            self.text_input.text += '\t{}\n'.format(os.path.join(path, filename))
            self.filelist.append(os.path.join(path, filename))
        self.dismiss_popup()

    def save(self, path, filename):        
        self.dismiss_popup()
        destination_file = open(os.path.join(path, filename), 'wb')
        merger = PdfFileMerger()
        self.text_input.text += 'Merging.'
        self.filelist.sort()
        for filesingle in self.filelist:
            self.text_input.text += '.'
            with open(filesingle, 'rb') as stream:
                merger.append(fileobj=stream)
        merger.write(destination_file)
        self.text_input.text += '\nMerge complete! \n'
        self.text_input.text += 'File saved at {}\n'.format(os.path.join(path, filename))
        self.text_input.text += ' - - - - - -  - - - - - - \n'



class PDFMergerApp(App):
    def build(self):
        self.icon = 'icon.png'


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)


if __name__ == '__main__':
    PDFMergerApp().run()