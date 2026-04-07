import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.label import Label
from utils import process_gallery

import logging
logging.getLogger("PIL").setLevel(logging.WARNING)

class GalleryApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # default paths
        if os.name == "posix" and not os.path.exists("/sdcard/DCIM"):
            DEFAULT_SOURCE = os.path.expanduser("~")
            DEFAULT_TARGET = os.path.expanduser("~/Downloads")
        else:
            DEFAULT_SOURCE = "/sdcard/DCIM"
            DEFAULT_TARGET = "/sdcard/Download"

        # FileChooser
        self.source_chooser = FileChooserIconView(path=DEFAULT_SOURCE)
        self.target_chooser = FileChooserIconView(path=DEFAULT_TARGET)

        # Show current path
        self.source_label = Label(text=self.source_chooser.path)
        self.target_label = Label(text=self.target_chooser.path)
        self.source_chooser.bind(path=lambda instance, value: setattr(self.source_label, 'text', value))
        self.target_chooser.bind(path=lambda instance, value: setattr(self.target_label, 'text', value))

        # Start sorting button
        run_button = Button(text="Start", size_hint=(1, 0.1))
        run_button.bind(on_press=self.run_sort)

        # Add widgets to layout
        layout.add_widget(self.source_label)
        layout.add_widget(self.source_chooser)
        layout.add_widget(self.target_label)
        layout.add_widget(self.target_chooser)
        layout.add_widget(run_button)

        return layout

    def run_sort(self, instance):
        source = self.source_chooser.path or "/sdcard/DCIM"
        target = self.target_chooser.path or "/sdcard/Download"
        process_gallery(source, target, verbose=True)

if __name__ == "__main__":
    GalleryApp().run()
