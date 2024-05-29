from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
# from main import VladimirApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

from controllers import register
from views import meta
from views.auth.auth import AuthScreen

Builder.load_file('views/registr/registr.kv')


class RegisterScreen(Screen):
    REGISTER_SCREEN = ObjectProperty()
    SCREEN_NAME = meta.SCREENS.REGISTER_SCREEN
    nickname = ObjectProperty()
    mail = ObjectProperty()
    pswrd = ObjectProperty()  # user's password
    warning = ObjectProperty()
    pswrd_repeat = ObjectProperty()
    reg = ObjectProperty()
    dialog = None

    def __init__(self, **kw):
        super().__init__(name=self.SCREEN_NAME, **kw)

    def switch_to_auth_screen(self):
        self.manager.current = meta.SCREENS.AUTH_SCREEN
        self.nickname.text = ''
        self.mail.text = ''
        self.pswrd.text = ''
        self.pswrd_repeat.text = ''

    def throw_dialog(self, text):
        dialog = self.dialog = MDDialog(
            text=f"[color=#000000][font=Roboto] {text}[/font] [/font][/color]"
        )
        dialog.open()

    def register(self):

        checked = True
        for element in self.mail.parent.parent.children[0].children:
            if not isinstance(element, MDTextField):
                continue
            if element.text == '':
                checked = False
                self.throw_dialog('Заполните всю форму!')
                break

        if checked:
            if self.pswrd.text != self.pswrd_repeat.text or self.pswrd.text == '':
                self.throw_dialog('Пароли не совпадают!')
                return
            response = register(user_data={
                    "nickname": self.nickname.text,
                    "password": self.pswrd.text,
                    "email": self.mail.text,
            })
            print(response)
            self.switch_to_auth_screen()
