import os
import logging

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from utils import process_gallery

logging.getLogger("PIL").setLevel(logging.WARNING)


class GalleryApp(App):
    def build(self):
        # Create main vertical layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Define default paths depending on platform
        if os.name == "posix" and not os.path.exists("/sdcard/DCIM"):
            DEFAULT_SOURCE = os.path.expanduser("~")
            DEFAULT_TARGET = os.path.expanduser("~")
        else:
            DEFAULT_SOURCE = "/sdcard/DCIM"
            DEFAULT_TARGET = "/sdcard/Download"

        # Store selected paths
        self.source = DEFAULT_SOURCE
        self.target = DEFAULT_TARGET

        # Source UI
        self.source_label = Label(text=f"Source: {self.source}")
        source_btn = Button(text="Select Source Folder")
        source_btn.bind(on_press=self.select_source)

        # Target UI
        self.target_label = Label(text=f"Target: {self.target}")
        target_btn = Button(text="Select Target Folder")
        target_btn.bind(on_press=self.select_target)

        # Start button
        start_btn = Button(text="Start", size_hint=(1, 0.2))
        start_btn.bind(on_press=self.run_sort)

        # Add widgets to layout
        layout.add_widget(self.source_label)
        layout.add_widget(source_btn)
        layout.add_widget(self.target_label)
        layout.add_widget(target_btn)
        layout.add_widget(start_btn)

        return layout

    # Open source folder selector
    def select_source(self, instance):
        self.open_filechooser("Select Source Folder", self.set_source)

    # Open target folder selector
    def select_target(self, instance):
        self.open_filechooser("Select Target Folder", self.set_target)

    # Open file chooser popup
    def open_filechooser(self, title, callback):
        chooser = FileChooserIconView(path=os.path.expanduser("~"))
        layout = BoxLayout(orientation='vertical')

        select_btn = Button(text="Select", size_hint=(1, 0.2))
        popup = Popup(title=title, content=layout, size_hint=(0.9, 0.9))

        # Handle folder selection
        def select_path(instance):
            selected_path = chooser.path
            callback(selected_path)
            popup.dismiss()

        select_btn.bind(on_press=select_path)

        layout.add_widget(chooser)
        layout.add_widget(select_btn)

        popup.open()

    # Set selected source path
    def set_source(self, path):
        self.source = path
        self.source_label.text = f"Source: {path}"

    # Set selected target path
    def set_target(self, path):
        self.target = path
        self.target_label.text = f"Target: {path}"

    # Run sorting process
    def run_sort(self, instance):
        process_gallery(self.source, self.target, verbose=True)


if __name__ == "__main__":
    # Run application
    GalleryApp().run()
