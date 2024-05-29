import requests
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import ThreeLineAvatarIconListItem, TwoLineAvatarIconListItem
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivymd.uix.tab import MDTabsBase
from pydantic import Json

from configs import URL, token
from views import meta
from controllers import get_current_user, get_companion, get_all_users, get_users_messages, get_friends

Builder.load_file('views/friends/friends.kv')


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class FriendsScreen(Screen):
    SCREEN_NAME = meta.SCREENS.FRIENDS_SCREEN

    def on_tab_switch(
            self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        if instance_tab.children[0].name == meta.SCREENS.FRIENDS_SEARCH_SCREEN:
            # instance_tab.children[0].children[0].children[0].init()
            pass
        else:
            instance_tab.children[0].children[0].init()
        print()

    def __init__(self, **kw):
        super().__init__(name=self.SCREEN_NAME, **kw)