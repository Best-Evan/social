from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRoundFlatButton
from pydantic import Json
from configs import URL
from controllers import send_invite, get_companion, get_current_user, get_friends, get_invites, get_sent_invites,\
    delete_friends, accept_invite, get_all_friends_requests, delete_request
from views import meta

Builder.load_file('views/friend_profile/friend_profile.kv')


def get_invite_id(invites: Json, companion: Json):
    current_user = get_current_user()
    if current_user.status_code == 404:
        return
    for key, value in invites.items():
        if value['user_sender'] == companion['id'] and value['user_receiver'] == current_user.json()['id']:
            return int(key)


def check_sent_request(companion: Json):
    sent_invites = get_sent_invites()
    if sent_invites.status_code == 404:
        return
    for key, invites in sent_invites.json().items():
        for invite in invites:
            if companion['nickname'] == invite:
                return True
    return False


def check_friend(companion: Json):
    friends = get_friends()
    if friends.status_code == 404:
        return
    if companion in friends.json():
        return True
    return False


def check_invites(companion: Json):
    invites = get_invites()
    if invites.status_code == 404:
        return
    for key, nicknames in invites.json().items():
        for nick in nicknames:
            if nick == companion['nickname']:
                return True
    return False


class FriendsProfileScreen(Screen):
    SCREEN_NAME = meta.SCREENS.FRIEND_PROFILE_SCREEN
    toolbar = ObjectProperty()
    #email = ObjectProperty()
    nickname = ObjectProperty()
    nick_text = ""
    email_text = ""
    add_friend = ObjectProperty()
    companion = None
    pfp = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(name=self.SCREEN_NAME, **kw)

    def init(self, companion: Json):
        self.companion = companion
        self.add_friend.text = 'Добавить в друзья'
        self.nickname.text = companion['nickname']
        self.pfp.source = f'{URL}/static/{self.nickname.text}.jpeg'
        self.toolbar.title = companion['nickname']
        if check_friend(companion=companion):
            self.add_friend.text = 'Удалить друга'
        if check_invites(companion=companion):
            self.add_friend.text = 'Принять заявку'
        if check_sent_request(companion=companion):
            self.add_friend.text = 'Отменить заявку'

    def go_back(self):
        MDApp.get_running_app().manager.current = meta.SCREENS.BASE_SCREEN

    def send_invite(self):
        if self.add_friend.text == 'Отменить заявку':
            current_user = get_current_user()
            requests = get_sent_invites()
            all_requests = get_all_friends_requests()
            req_id = None
            for key, value in all_requests.json().items():
                if value['user_sender'] == current_user.json()['id']:
                    req_id = int(key)
            delete_request(request_id=req_id)
            self.add_friend.text = 'Добавить в друзья'
            return

        if self.add_friend.text == 'Принять заявку':
            all_invites = get_all_friends_requests().json()
            invite_id = get_invite_id(invites=all_invites, companion=self.companion)
            accept_invite(invite_id)
            self.add_friend.text = 'Удалить друга'
            return
        if self.add_friend.text == 'Удалить друга':
            delete_friends(int(self.companion['id']))
            self.add_friend.text = 'Добавить в друзья'
            return
        if self.add_friend.text == 'Добавить в друзья':
            user = get_companion(self.toolbar.title)
            send_invite(user.json()['id'])
            self.add_friend.text = 'Отменить заявку'
            return