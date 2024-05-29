from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineAvatarIconListItem, ImageLeftWidget

from configs import URL
from controllers import get_posts, add_post, get_invites, get_friends, get_current_user
from views import meta
global_post_text = ""
Builder.load_file('views/news/news.kv')

# KV = '''
# <Content>
#     orientation: "vertical"
#     spacing: "12dp"
#     size_hint_y: None
#     height: "120dp"
#
#     MDTextField:
#         id:add_post_textfield
# '''
class ImageItem(ThreeLineAvatarIconListItem):
    image = ObjectProperty()
    def __init__(self,source_img, post_t, post_tt, **kwargs):
        super(ImageItem, self).__init__(**kwargs)
        self.image_source = source_img
        self.post_text = post_t
        self.post_tertiary_text = f"[color=#000000][font=Roboto] {post_tt}[/font] [/font][/color]"
    def post_show(self):
        MDApp.get_running_app().manager.news_screen.post_show(self.post_tertiary_text)
class Content(BoxLayout):
    pass

# class MyPost():
#     list_view = ObjectProperty()
#
#     def my_post(self):
#         self.text = ''
#         self.list_view.add_widget(ThreeLineAvatarIconListItem(
#             text=post['username'], on_press=self.post_show,
#             secondary_text='data',
#             tertiary_text=f"[color=#000000][font=Roboto]{self.text}[/font] [/font][/color]",
#         ))
class NewsScreen(Screen):
    SCREEN_NAME = meta.SCREENS.NEWS_SCREEN
    dialog = None
    post = ObjectProperty()
    list_view = ObjectProperty()
    add_post_textfield = ObjectProperty()
    def __init__(self, **kw):
        super().__init__(name=self.SCREEN_NAME, **kw)

    def init(self, *args):
        self.close_button = MDFlatButton(text="Close", on_release=self.d_close)
        self.dialog = None
        self.list_view.clear_widgets()
        posts = get_posts()
        friends = get_friends()
        me = get_current_user()
        output_posts = []
        posts_usernames = []
        for key, value in posts.json().items():
            if value['username'] == me.json()['nickname']:
                if value in output_posts:
                    continue
                else:
                    output_posts.append(value)
                posts_usernames.append(value['username'])
        for friend in friends.json():
            for key, value in posts.json().items():
                if value['username'] == friend['nickname'] or value['username'] == me.json()['nickname']:
                    if value in output_posts:
                        continue
                    else:
                        output_posts.append(value)
                        posts_usernames.append(value['username'])
        for post in output_posts:
            global_post_text = posts_usernames.pop(0)
            self.list_view.add_widget(ImageItem(source_img=f"{URL}/static/{global_post_text}.jpeg", post_t=post['username'], post_tt=post['content']))
            # self.list_view.add_widget(ThreeLineAvatarIconListItem(
            #     text=post['username'], on_press=self.post_show,
            #     tertiary_text=f"[color=#000000][font=Roboto]{post['content']}[/font] [/font][/color]",
            #
            #))

    def posts_show(self, *args):
        for post in self.response.json().values():
            post_text = post['username']
            post_content = post['content']
            self.post_change(post_text, post_content)


    # def on_enter(self, *args):
    #     print("jopa")
    #

    def post_show(self,post_text, *args):
        self.build(instance=args)
        posts = get_posts()
        close_button = MDFlatButton(text="Close", on_release=self.d_close),
        self.dialog_text = post_text
        for key, value in posts.json().items():
            if not self.dialog:
                self.dialog = MDDialog(
                    text=f"[color=#000000][font=Roboto] {self.dialog_text}[/font] [/font][/color]",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            theme_text_color="Custom",
                            on_release=self.d_close
                        ),]
                )
            self.dialog.open()
    # функция открытия окна добавления поста
    def show(self):
        MDApp.get_running_app().manager.current = meta.SCREENS.ADD_POSTS_SCREEN


    #фунция отправлющая пост запрос на сервер обновляя страницу
    # def posting(self, *args):
    #     add_post(self.add_post_textfield.text)
    #     self.list_view.clear_widgets()
    #     self.init()
    #     self.d_close(instance=args)

    def d_close(self, *args):
        self.dialog.dismiss(force=True)
        self.init()
    #загрузка параметров из файла dialog_plus
    def build(self, instance):
        return Builder.load_file("views/content.kv")