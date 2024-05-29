import os.path

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from controllers import get_all_users, decode_image
from views import meta

Builder.load_file('views/base.kv')


class BaseScreen(Screen):
    SCREEN_NAME = 'base'

    def on_tab_press(self, *args):
        screens = self.children[0].children[1].screens

        for item in screens:
            if item.name == meta.SCREENS.PROFILE_SCREEN or item.name == meta.SCREENS.NEWS_SCREEN:
                item.children[0].init()
            if item.name == meta.SCREENS.MESSAGES_SCREEN:
                item.children[0].children[0].init()
            if item.name == meta.SCREENS.FRIENDS_SCREEN:
                friends_list = \
                item.children[0].children[0].children[1].children[0].children[0].children[0].children[0].children[0]
                if type(friends_list) == BoxLayout:
                    return
                friends_list.init()
            # if item.name == meta.SCREENS.ADD_POSTS_SCREEN:
            #     item.children[1].children[1].children[1].switch_on_add_posts()
    def __init__(self, **kw):
        super().__init__(name=self.SCREEN_NAME, **kw)
