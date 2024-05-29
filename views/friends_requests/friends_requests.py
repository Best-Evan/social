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

from configs import URL
from views import meta
from controllers import get_current_user, get_companion, get_all_users, get_users_messages, get_friends, get_invites

Builder.load_file('views/friends_requests/friends_requests.kv')


class NewRecycleContainer(LayoutSelectionBehavior,
                  RecycleBoxLayout):
    pass


class Requests(RecycleDataViewBehavior, TwoLineAvatarIconListItem):
    index = None
    pfp = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.pfp.source = data['url']
        return super(Requests, self).refresh_view_attrs(
            rv, index, data)

    def show_profile(self):
        companion = get_companion(self.text)
        base = MDApp.get_running_app().manager.get_screen(meta.SCREENS.BASE_SCREEN)
        friend = base.manager.children[0].manager.screens[9]
        friend.init(
            companion.json()
        )
        MDApp.get_running_app().manager.current = meta.SCREENS.FRIEND_PROFILE_SCREEN


class ResyView(RecycleView):
    def __init__(self, **kwargs):
        super(ResyView, self).__init__(**kwargs)

    def init(self):
        self.data = {}
        invites = get_invites()
        if invites.status_code == 404:
            return
        for key, invites in invites.json().items():
            for invite in invites:
                self.data.append({
                    'text': invite,
                    'url': f'{URL}/static/{invite}.jpeg'
                })


class FriendsRequestsScreen(Screen):
    SCREEN_NAME = meta.SCREENS.FRIENDS_REQUESTS_SCREEN

    def __init__(self, **kw):
        super().__init__(name=self.SCREEN_NAME, **kw)