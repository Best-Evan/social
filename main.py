from kivy.core.window import Window
from kivymd.app import MDApp

from screen_manager import Manager

Window.size = (450, 650)


class ValeraApp(MDApp):
    def build(self):
        self.manager = Manager()
        return self.manager


if __name__ == '__main__':
    ValeraApp().run()
