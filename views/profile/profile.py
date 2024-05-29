from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from configs.token import token
from configs import URL
from controllers import network_methods
from views import meta

Builder.load_file('views/profile/profile.kv')


class ProfileScreen(Screen):
    SCREEN_NAME = meta.SCREENS.PROFILE_SCREEN
    nickname: Label = ObjectProperty()
    pfp = AsyncImage()
    nick_text = ""
    email_text = ""

    def __init__(self, **kw):
        super().__init__(name=self.SCREEN_NAME, **kw)

    def init(self):
        data = network_methods.get_current_user().json()
        self.nick_text = data["nickname"]
        self.nickname.text = self.nick_text
        self.pfp.source = f'{URL}/static/{data["nickname"]}.jpeg'
        self.pfp.reload()

    def switch_to_edit_screen(self):
        MDApp.get_running_app().manager.current = meta.SCREENS.EDIT_PROFILE_SCREEN

    def on_enter(self, *args):
        super().on_enter(*args)
        print(1)

    def log_out(self):
        token.clear()
        MDApp.get_running_app().manager.current = meta.SCREENS.AUTH_SCREEN

