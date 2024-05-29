from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.textfield import MDTextField

from configs import URL
from controllers import network_methods, encode_image
from views import meta

Builder.load_file('views/profile_edit/edit.kv')


class EditScreen(Screen):
    SCREEN_NAME = meta.SCREENS.EDIT_PROFILE_SCREEN
    login: MDTextField = ObjectProperty()
    email: MDTextField = ObjectProperty()
    pwd: MDTextField = ObjectProperty()
    save: MDRoundFlatButton = ObjectProperty()
    cancel: MDRoundFlatButton = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(name=self.SCREEN_NAME, **kw)
        self.manager_open = False
        self.img = None
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )

    def switch_to_base_screen(self):
        MDApp.get_running_app().manager.current = meta.SCREENS.BASE_SCREEN
        self.login.text = ''
        self.email.text = ''
        self.pwd.text = ''

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        self.img = path
        self.exit_manager()


    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def apply_changes(self):

        output_json = {}
        if self.login.text != '':
            output_json['nickname'] = self.login.text
        else:
            output_json['nickname'] = None
        if self.email.text != '':
            output_json['email'] = self.email.text
        else:
            output_json['email'] = None
        if self.pwd.text != '':
            output_json['password'] = self.pwd.text
        else:
            output_json['password'] = None

        if self.img is not None:
            with open(self.img, 'rb') as image:
                new_pfp = image.read()
            output_json['avatar'] = encode_image(new_pfp)

        response = network_methods.send_new_profile_data(
            user_data=output_json
        )

        if response.status_code == 200:
            base = MDApp.get_running_app().manager.get_screen(meta.SCREENS.BASE_SCREEN)
            base.children[0].children[1].screens[3].children[0].init()
            self.switch_to_base_screen()
