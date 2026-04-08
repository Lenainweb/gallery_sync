import os
import logging
import threading
import sys

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from utils import process_gallery

logging.getLogger("PIL").setLevel(logging.WARNING)


class GalleryApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Default paths
        if os.name == "posix" and not os.path.exists("/sdcard/DCIM"):
            DEFAULT_SOURCE = os.path.expanduser("~")
            DEFAULT_TARGET = os.path.expanduser("~")
        else:
            DEFAULT_SOURCE = "/sdcard/DCIM"
            DEFAULT_TARGET = "/sdcard/Download"

        self.source = DEFAULT_SOURCE
        self.target = DEFAULT_TARGET

        # Source
        self.source_label = Label(text=f"Source: {self.source}")
        source_btn = Button(text="Select Source Folder")
        source_btn.bind(on_press=self.select_source)

        # Target
        self.target_label = Label(text=f"Target: {self.target}")
        target_btn = Button(text="Select Target Folder")
        target_btn.bind(on_press=self.select_target)

        # Status
        self.status_label = Label(text="Status: Idle")

        # Log output
        self.log_output = TextInput(size_hint=(1, 0.5), readonly=True)

        # Start button
        start_btn = Button(text="Start", size_hint=(1, 0.2))
        start_btn.bind(on_press=self.run_sort)

        # Layout
        layout.add_widget(self.source_label)
        layout.add_widget(source_btn)
        layout.add_widget(self.target_label)
        layout.add_widget(target_btn)
        layout.add_widget(self.status_label)
        layout.add_widget(self.log_output)
        layout.add_widget(start_btn)

        return layout

    def select_source(self, instance):
        self.open_filechooser("Select Source Folder", self.set_source)

    def select_target(self, instance):
        self.open_filechooser("Select Target Folder", self.set_target)

    def open_filechooser(self, title, callback):
        chooser = FileChooserIconView(path=os.path.expanduser("~"))
        layout = BoxLayout(orientation='vertical')

        select_btn = Button(text="Select", size_hint=(1, 0.2))
        popup = Popup(title=title, content=layout, size_hint=(0.9, 0.9))

        def select_path(instance):
            callback(chooser.path)
            popup.dismiss()

        select_btn.bind(on_press=select_path)

        layout.add_widget(chooser)
        layout.add_widget(select_btn)

        popup.open()

    def set_source(self, path):
        self.source = path
        self.source_label.text = f"Source: {path}"

    def set_target(self, path):
        self.target = path
        self.target_label.text = f"Target: {path}"

    def run_sort(self, instance):
        # Run in separate thread to avoid UI freeze
        threading.Thread(target=self.process_with_ui).start()

    def process_with_ui(self):
        # Update status
        Clock.schedule_once(lambda dt: self.update_status("Processing..."))

        # Redirect print to UI
        old_stdout = sys.stdout
        sys.stdout = self

        try:
            process_gallery(self.source, self.target, verbose=True)
            Clock.schedule_once(lambda dt: self.update_status("Done"))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status(f"Error: {e}"))
        finally:
            sys.stdout = old_stdout

    # Capture print() output
    def write(self, message):
        Clock.schedule_once(lambda dt: self.append_log(message))

    def flush(self):
        pass

    def append_log(self, text):
        self.log_output.text += text

    def update_status(self, text):
        self.status_label.text = f"Status: {text}"

def main():
    GalleryApp().run()

if __name__ == "__main__":
    main()
