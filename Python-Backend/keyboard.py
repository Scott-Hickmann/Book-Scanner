from pynput import keyboard
from pynput.keyboard import Key, KeyCode


class Keyboard:
    def __init__(self):
        self.key = None
        self.start()

    def start(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        self.listener.start()

    def stop(self):
        self.listener.stop()

    def has_pressed(self, key):
        if self.key is None:
            return False
        if self.key == key:
            self.key = None
            return True
        return False

    def on_press(self, key):
        self.key = key

    def on_release(self, key):
        pass
        # print(f"{key} released")
        # self.key = None
