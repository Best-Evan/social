from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from controllers import network_methods
from threading import Timer
from kivy.core.window import Window

from kivymd.uix.label import MDLabel
from views import meta


Builder.load_file('views/dialog/dialog.kv')

second_user = None


class DialogMessage(MDBoxLayout):
    def __init__(self, text="fak.sjdf", is_mine=False, **kwargs):
        super(DialogMessage, self).__init__(**kwargs)
        self.msg_text = text
        self.is_mine = is_mine


class DialogScreen(Screen):
    SCREEN_NAME = meta.SCREENS.DIALOG_SCREEN
    message_container = ObjectProperty()
    text_field = ObjectProperty()
    scroll_view = ObjectProperty()
    current_user = None
    companion = None

    def __init__(self, **kw):
        super().__init__(name=self.SCREEN_NAME, **kw)
        self.max_message_id = -1
        self.min_message_id = 1000
        self.run = False
        self.already_fetching = False
        Window.bind(on_request_close=self.on_close)
        # self.bind(self.scroll_view.on_scroll_start=self.update_scroll)

    def on_close(self, *args):
        self.run = False

    def update_scroll(self):
        if self.scroll_view.scroll_y >= 1 and not self.already_fetching:
            self.already_fetching = True
            cur_user = network_methods.get_current_user().json()["id"]
            data = network_methods.get_messages_less(cur_user, second_user, self.min_message_id)
            self.parse_to_begin(data.json())
            self.already_fetching = False

    def test(self):
        if self.run is not None and self.run:
            self.update_messages()
            Timer(1, self.test).start()

    def on_pre_enter(self):
        self.load_last_messages()
        self.run = True
        self.test()
        if len(self.scroll_view.children) != 0:
            self.scroll_view.scroll_to(self.scroll_view.children[-1])

    def on_leave(self, *args):
        self.min_message_id = 1000
        self.max_message_id = -1
        self.run = False
        self.message_container.clear_widgets()

    def load_last_messages(self):
        cur_user = network_methods.get_current_user().json()["id"]
        data = network_methods.get_messages_last(cur_user, second_user).json()
        if len(data["sender"]) != 0:
            self.min_message_id = min(self.min_message_id, data["sender"][0]["id"])
        if len(data["receiver"]) != 0:
            self.min_message_id = min(self.min_message_id, data["receiver"][0]["id"])
        self.parse_to_end(data)

    def update_messages(self):
        cur_user = network_methods.get_current_user().json()["id"]
        data = network_methods.get_messages_greater(cur_user, second_user, self.max_message_id).json()
        # self.min_message_id = min(data["sender"][0]["id"], data["receiver"][0]["id"])
        self.parse_to_end(data)

    def parse_to_end(self, data):
        sender_arr = data["sender"]
        receiver_arr = data["receiver"]
        l, r = 0, 0  # l - sender, r - receiver
        while l < len(sender_arr) or r < len(receiver_arr):
            if l == len(sender_arr) and len(receiver_arr) > 0:
                self.message_container.add_widget(DialogMessage(receiver_arr[r]["content"], is_mine=True))
                self.max_message_id = receiver_arr[r]["id"]
                r += 1
            elif r == len(receiver_arr):
                self.message_container.add_widget(DialogMessage(text=sender_arr[l]["content"], is_mine=False))
                #self.message_container.add_widget(Label(text=sender_arr[l]['content']))
                self.max_message_id = sender_arr[l]["id"]
                l += 1
            elif len(sender_arr) > 0 and len(receiver_arr) > 0 and sender_arr[l]["id"] < receiver_arr[r]["id"]:
                self.message_container.add_widget(DialogMessage(sender_arr[l]["content"], is_mine=False))
                self.max_message_id = sender_arr[l]["id"]
                l += 1
            else:
                self.message_container.add_widget(DialogMessage(receiver_arr[r]["content"], is_mine=True))
                self.max_message_id = receiver_arr[r]["id"]
                r += 1

    def parse_to_begin(self, data):
        sender_arr = data["sender"]
        receiver_arr = data["receiver"]
        l, r = 0, 0  # l - sender, r - receiver
        while l < len(sender_arr) or r < len(receiver_arr):
            if l == len(sender_arr):
                self.message_container.add_widget(DialogMessage(receiver_arr[r]["content"], is_mine=True), len(self.scroll_view.children[0].children))
                self.min_message_id = receiver_arr[r]["id"]
                r += 1
            elif r == len(receiver_arr):
                self.message_container.add_widget(DialogMessage(sender_arr[l]["content"], is_mine=False), len(self.scroll_view.children[0].children))
                self.min_message_id = sender_arr[l]["id"]
                l += 1
            elif sender_arr[l]["id"] < receiver_arr[r]["id"]:
                self.message_container.add_widget(DialogMessage(sender_arr[l]["content"], is_mine=False), len(self.scroll_view.children[0].children))
                self.min_message_id = sender_arr[l]["id"]
                l += 1
            else:
                self.message_container.add_widget(DialogMessage(receiver_arr[r]["content"], is_mine=True), len(self.scroll_view.children[0].children))
                self.min_message_id = receiver_arr[r]["id"]
                r += 1

    def send_message(self):
        network_methods.send_message(receiver_id=int(second_user), text=self.text_field.text)
        print()
        self.text_field.text = ""
        #self.scroll_view.scroll_to(self.scroll_view.children[len(self.scroll_view.children)])

    def close_dialog(self):
        MDApp.get_running_app().manager.current = meta.SCREENS.BASE_SCREEN
