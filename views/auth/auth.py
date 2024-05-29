from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from views import meta
from configs import token
from controllers import sing_in, get_all_users, decode_image
from views.friends_list.friends_list import ResView

Builder.load_file('views/auth/auth.kv')


class AuthScreen(Screen):
    SCREEN_NAME = meta.SCREENS.AUTH_SCREEN
    login = ObjectProperty()
    pswrd = ObjectProperty()
    warning = ObjectProperty()
    reg_but = ObjectProperty()
    REGISTR_SCREEN = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(name=self.SCREEN_NAME, **kw)

    def authorization(self):

        response = sing_in(login=self.login.text, password=self.pswrd.text)
        print(response.json())

        if response:
            print(self.manager)
            self.manager.current = meta.SCREENS.BASE_SCREEN
            token.update({'token': response.json()['access_token']})
            base = MDApp.get_running_app().manager.get_screen(meta.SCREENS.BASE_SCREEN)
            self.login.text = ''
            self.pswrd.text = ''
            self.warning.text = ''
            self.login.text = ''
            base.on_tab_press(self)
        else:
            self.warning.text = 'Неверный email или пароль!'

    def switch_to_reg_screen(self):
        self.manager.current = meta.SCREENS.REGISTER_SCREEN
        self.login.text = ''
        self.pswrd.text = ''
        self.warning.text = ''
        self.login.text = ''
