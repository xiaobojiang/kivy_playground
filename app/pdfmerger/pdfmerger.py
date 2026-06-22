from kivy.config import Config

# On desktop (especially macOS), Ctrl+click can trigger Kivy's multitouch
# simulator and leave a red touch marker; disable that input mode.
Config.set('input', 'mouse', 'mouse,disable_multitouch')

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
    load_all = ObjectProperty(None)
    remove = ObjectProperty(None)
    clear = ObjectProperty(None)
    cancel = ObjectProperty(None)
    homepath = StringProperty(str(Path.home()))


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    homepath = StringProperty(str(Path.home()))

    def use_selected_name(self, selection):
        if selection:
            self.text_input.text = os.path.basename(selection[0])


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    last_selected_dir = StringProperty(str(Path.home()))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filelist = []

    def dismiss_popup(self):
        self._popup.dismiss()

    def _refresh_loaded_files_text(self, action_message=''):
        self.text_input.text = 'You have selected following {} files: \n'.format(len(self.filelist))
        for file_path in sorted(self.filelist):
            self.text_input.text += '\t{}\n'.format(file_path)
        if action_message:
            self.text_input.text += '{}\n'.format(action_message)

    def show_load(self):
        content = LoadDialog(
            load=self.load,
            load_all=self.load_all_from_folder,
            remove=self.remove_loaded_files,
            clear=self.clear_loaded_files,
            cancel=self.dismiss_popup,
            homepath=self.last_selected_dir,
        )
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(
            save=self.save,
            cancel=self.dismiss_popup,
            homepath=self.last_selected_dir,
        )
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filenames):
        if not filenames:
            self.text_input.text += 'No file selected.\n'
            self.dismiss_popup()
            return

        self.last_selected_dir = os.path.abspath(path)

        added_count = 0
        for filename in filenames:
            full_path = os.path.abspath(os.path.join(path, filename))
            if full_path not in self.filelist:
                self.filelist.append(full_path)
                added_count += 1

        self._refresh_loaded_files_text('Added {} new file(s).'.format(added_count))
        self.dismiss_popup()

    def load_all_from_folder(self, path):
        if not path:
            self.text_input.text += 'No folder selected.\n'
            return

        folder = os.path.abspath(path)
        self.last_selected_dir = folder

        try:
            pdf_files = []
            for name in os.listdir(folder):
                full_path = os.path.join(folder, name)
                if os.path.isfile(full_path) and name.lower().endswith('.pdf'):
                    pdf_files.append(full_path)
        except Exception as exc:
            self.text_input.text += 'Failed to read folder: {}\n'.format(exc)
            return

        if not pdf_files:
            self.text_input.text += 'No PDF files found in current folder.\n'
            return

        added_count = 0
        for full_path in sorted(pdf_files):
            if full_path not in self.filelist:
                self.filelist.append(full_path)
                added_count += 1

        self._refresh_loaded_files_text('Added {} file(s) from folder.'.format(added_count))
        self.dismiss_popup()

    def remove_loaded_files(self, path, filenames):
        if not filenames:
            self.text_input.text += 'No file selected to remove.\n'
            return

        self.last_selected_dir = os.path.abspath(path)
        removed_count = 0
        for filename in filenames:
            full_path = os.path.abspath(os.path.join(path, filename))
            if full_path in self.filelist:
                self.filelist.remove(full_path)
                removed_count += 1

        self._refresh_loaded_files_text('Removed {} file(s).'.format(removed_count))

    def clear_loaded_files(self):
        cleared_count = len(self.filelist)
        self.filelist = []
        self._refresh_loaded_files_text('Cleared {} file(s).'.format(cleared_count))
        self.dismiss_popup()

    def save(self, path, filename):        
        self.dismiss_popup()
        self.last_selected_dir = os.path.abspath(path)
        if not self.filelist:
            self.text_input.text += 'Please load at least one PDF before merging.\n'
            return

        output_name = filename.strip() if filename else ''
        if not output_name:
            output_name = 'merged.pdf'
        if not output_name.lower().endswith('.pdf'):
            output_name += '.pdf'

        destination_path = os.path.join(path, output_name)
        merger = PdfFileMerger()

        try:
            self.text_input.text += 'Merging.'
            for filesingle in sorted(self.filelist):
                self.text_input.text += '.'
                with open(filesingle, 'rb') as stream:
                    merger.append(fileobj=stream)

            with open(destination_path, 'wb') as destination_file:
                merger.write(destination_file)

            self.text_input.text += '\nMerge complete! \n'
            self.text_input.text += 'File saved at {}\n'.format(destination_path)
            self.text_input.text += ' - - - - - -  - - - - - - \n'
        except Exception as exc:
            self.text_input.text += '\nMerge failed: {}\n'.format(exc)
        finally:
            merger.close()



class PDFMergerApp(App):
    def build(self):
        self.icon = 'icon.png'


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)


if __name__ == '__main__':
    PDFMergerApp().run()