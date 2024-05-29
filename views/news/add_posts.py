from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineAvatarIconListItem
from controllers import get_posts, add_post
from views import meta
Builder.load_file('views/news/add_posts.kv')


class Content(BoxLayout):
    pass


class Add_Posts_Screen(Screen):
    SCREEN_NAME = meta.SCREENS.ADD_POSTS_SCREEN
    add_post_textfield = ObjectProperty()
    add_post_but = ObjectProperty()
    back_to_news_but = ObjectProperty()
    def __init__(self, **kw):
        super().__init__(name=self.SCREEN_NAME, **kw)


    def posts_show(self, *args):
        for post in self.response.json().values():
            post_text = post['username']
            post_content = post['content']
            self.post_change(post_text, post_content)


    def posting(self):
        self.manager.current = meta.SCREENS.BASE_SCREEN
        add_post(self.add_post_textfield.text)
        base = MDApp.get_running_app().manager.get_screen(meta.SCREENS.BASE_SCREEN)
        base.on_tab_press(self)


    def back_to_news(self):
        MDApp.get_running_app().manager.current = meta.SCREENS.BASE_SCREEN