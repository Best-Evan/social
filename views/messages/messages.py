import requests
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineAvatarIconListItem
from pydantic import Json

from configs import URL
from controllers import get_current_user, get_companion, get_all_users, get_users_messages, get_friends
from views import meta
from views.dialog import dialog
from controllers import get_current_user, get_companion, get_all_users

Builder.load_file('views/messages/messages.kv')


class RecycleCont(LayoutSelectionBehavior,
                  RecycleBoxLayout):
    pass


class Message(RecycleDataViewBehavior, TwoLineAvatarIconListItem):
    user_id = None
    pfp = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.user_id = data["id"]
        self.pfp.source = data['url']
        return super(Message, self).refresh_view_attrs(
            rv, index, data)

    def show_dialog(self):
        current_user = get_current_user()
        companion = get_companion(self.text)
        dialog.second_user = self.user_id
        # MDApp.get_running_app().manager.transition.direction = 'left'
        MDApp.get_running_app().manager.current = meta.SCREENS.DIALOG_SCREEN


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

    def get_max_message(self, messages: Json):
        max_id: int = 0
        max_message = None
        for message in messages['sender']:
            if int(message['id']) > max_id:
                max_id = int(message['id'])
                max_message = message
        for message in messages['receiver']:
            if int(message['id']) > max_id:
                max_id = int(message['id'])
                max_message = message
        if max_message is None:
            return ''
        return max_message['content']

    def init(self):
        self.data = {}
        try:
            users = get_friends()
            current_user = get_current_user()
        except requests.exceptions.ConnectionError:
            raise requests.exceptions.ConnectionError('Server connection failed')

        for user in users.json():
            messages = get_users_messages(sender_id=current_user.json()['id'], receiver_id=user['id'])
            last_message = self.get_max_message(messages=messages.json())
            self.data.append({
                "text": user['nickname'],
                "secondary_text": last_message,
                'url': f'{URL}/static/{user["nickname"]}.jpeg',
                "id": user["id"]
            })


class MessagesScreen(Screen):
    SCREEN_NAME = meta.SCREENS.MESSAGES_SCREEN

    def __init__(self, **kw):
        super().__init__(name=self.SCREEN_NAME, **kw)
