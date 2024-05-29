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
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivymd.uix.tab import MDTabsBase
from pydantic import Json

from configs import URL, token
from views import meta
from controllers import get_current_user, get_companion, get_all_users, get_users_messages, get_friends

Builder.load_file('views/friends_list/friends_list.kv')


class RecycleContainer(LayoutSelectionBehavior,
                  RecycleBoxLayout):
    pass


class Friend(RecycleDataViewBehavior, TwoLineAvatarIconListItem):
    index = None
    pfp = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.pfp.source = data['url']
        return super(Friend, self).refresh_view_attrs(
            rv, index, data)

    def show_profile(self):
        companion = get_companion(self.text)
        base = MDApp.get_running_app().manager.get_screen(meta.SCREENS.BASE_SCREEN)
        friend = base.manager.children[0].manager.screens[9]
        friend.init(
            companion.json()
        )
        MDApp.get_running_app().manager.current = meta.SCREENS.FRIEND_PROFILE_SCREEN


class ResView(RecycleView):

    def __init__(self, **kwargs):
        super(ResView, self).__init__(**kwargs)

    @staticmethod
    def get_friends_nickname(friends: list):
        try:
            nicknames = [friend['nickname'] for friend in friends]
            return nicknames
        except TypeError:
            return

    def init(self):
        self.data = {}
        try:
            user_friends = get_friends()
            if user_friends.status_code == 404:
                return
            friends = self.get_friends_nickname(user_friends.json())
            print(friends)
            for friend in friends:
                self.data.append({
                    'text': friend,
                    'url': f'{URL}/static/{friend}.jpeg'
                })
        except TypeError:
            return


class FriendsListScreen(Screen):
    SCREEN_NAME = meta.SCREENS.FRIENDS_LIST_SCREEN

    def __init__(self, **kw):
        super().__init__(name=self.SCREEN_NAME, **kw)