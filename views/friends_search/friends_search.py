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
from controllers import get_current_user, get_companion, get_all_users, get_users_messages, get_friends, get_invites

Builder.load_file('views/friends_search/friends_search.kv')


def search_person(users: list, text: str) -> list:
    res = []
    for word in users:
        word_list = list(word)
        word_list = word_list[0:len(text)]
        if text == ''.join(word_list).lower():
            res.append(word)
    return res


class RViewContainer(LayoutSelectionBehavior,
                  RecycleBoxLayout):
    pass


class Search(RecycleDataViewBehavior, TwoLineAvatarIconListItem):
    index = None
    pfp = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.pfp.source = data['url']
        return super(Search, self).refresh_view_attrs(
            rv, index, data)

    def show_profile(self):
        companion = get_companion(self.text)
        base = MDApp.get_running_app().manager.get_screen(meta.SCREENS.BASE_SCREEN)
        friend = base.manager.children[0].manager.screens[9]
        friend.init(
            companion.json()
        )
        MDApp.get_running_app().manager.current = meta.SCREENS.FRIEND_PROFILE_SCREEN


class RView(RecycleView):
    def __init__(self, **kwargs):
        super(RView, self).__init__(**kwargs)

    def search(self, text: str):
        self.data = {}
        all_users = get_all_users()
        current_user = get_current_user()
        users = []
        for user in all_users.json():
            users.append(user['nickname'])
        found_users = search_person(users=users, text=text)
        if not found_users:
            return
        f = current_user.json()['nickname']
        for user in found_users:
            if user == f:
                pass
            else:
                self.data.append({
                    'text': user,
                    'url': f'{URL}/static/{user}.jpeg'
                })


class FriendsSearchScreen(Screen):
    SCREEN_NAME = meta.SCREENS.FRIENDS_SEARCH_SCREEN
    search = ObjectProperty()

    def search_friends(self):
        self.children[0].children[0].search(self.search.text)

    def __init__(self, **kw):
        super().__init__(name=self.SCREEN_NAME, **kw)
        print()