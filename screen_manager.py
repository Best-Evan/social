from kivy.uix.screenmanager import ScreenManager
from views.news.news import NewsScreen
from views.messages.messages import MessagesScreen
from views.profile_edit.edit import EditScreen
from views.profile.profile import ProfileScreen
from views.auth.auth import AuthScreen
from views.base import BaseScreen
from views.registr.registr import RegisterScreen
from views.dialog.dialog import DialogScreen
from views.friends.friends import FriendsScreen
from views.friend_profile.friend_profile import FriendsProfileScreen
from views.friends_requests.friends_requests import FriendsRequestsScreen
from views.friends_search.friends_search import FriendsSearchScreen
from views.friends_list.friends_list import FriendsListScreen
from views.news.add_posts import Add_Posts_Screen
from views.news.news import ImageItem

class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.news_screen = NewsScreen()
        self.add_widget(AuthScreen())
        self.add_widget(BaseScreen())
        self.add_widget(EditScreen())
        self.add_widget(self.news_screen)
        self.add_widget(MessagesScreen())
        self.add_widget(ProfileScreen())
        self.add_widget(RegisterScreen())
        self.add_widget(DialogScreen())
        self.add_widget(FriendsScreen())
        self.add_widget(FriendsProfileScreen())
        self.add_widget(FriendsRequestsScreen())
        self.add_widget(FriendsSearchScreen())
        self.add_widget(FriendsListScreen())
        self.add_widget(Add_Posts_Screen())