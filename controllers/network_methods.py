import json

import requests
from requests import Response

from configs import token, URL


def get_friends() -> Response:
    response = requests.get(
        f"{URL}/friends/",
        headers={'Authorization': f"Bearer {token['token']}"}
    )
    return response


def add_post(content:str):
    responce = requests.post(
        f"{URL}/users/posts",
        json={"content": content},
        headers={'Authorization': f"Bearer {token['token']}"}
    )
    return responce

def get_posts():
    response = requests.get(
        f"{URL}/posts"
    )

    return response


def get_current_user() -> Response:
    response = requests.get(
        f"{URL}/user/me",
        headers={'Authorization': f"Bearer {token['token']}"}
    )
    return response


def get_messages_greater(sender_id: int, receiver_id: int, id: int):
    messages = requests.get(
        f"{URL}/messages/upd?sender_id={sender_id}&receiver_id={receiver_id}&id={id}",
        headers={'Authorization': f"Bearer {token['token']}"}
    )
    return messages


def get_messages_less(sender_id: int, receiver_id: int, id: int):
    messages = requests.get(
        f"{URL}/messages/prev?sender_id={sender_id}&receiver_id={receiver_id}&id={id}",
        headers={'Authorization': f"Bearer {token['token']}"}
    )
    return messages

def get_messages_last(sender_id: int, receiver_id: int):
    messages = requests.get(
        f"{URL}/messages/last?sender_id={sender_id}&receiver_id={receiver_id}",
        headers={'Authorization': f"Bearer {token['token']}"}
    )
    return messages


def get_companion(nickname: str) -> Response:
    response = requests.get(
        f"{URL}/users/get/{nickname}"
    )
    return response


def get_all_users() -> Response:
    users: Response = requests.get(f"{URL}/users")
    return users


def get_users_messages(sender_id: int, receiver_id: int):
    messages = requests.get(
        f"{URL}/messages?sender_id={sender_id}&receiver_id={receiver_id}",
        headers={'Authorization': f"Bearer {token['token']}"}
    )
    return messages


def sing_in(login: str, password: str) -> Response:
    token = requests.post(
            f'{URL}/token',
            data={
                'grant_type': '', 'username': login,
                'password': password, 'scope': '',
                'client_id': '', 'client_secret': ''
            })
    return token


def send_invite(id: int):
    response = requests.post(
        f'{URL}/friend/invite?rec_id={id}',
        headers={'Authorization': f"Bearer {token['token']}"}
    )
    return response


def get_invites():
    response = requests.get(
        f"{URL}/friends/requests",
        headers={'Authorization': f"Bearer {token['token']}"}
    )
    return response


def get_sent_invites() -> Response:
    response = requests.get(
        f"{URL}/friends/sent/invites",
        headers={'Authorization': f"Bearer {token['token']}"}
    )
    return response


def delete_friends(friend_id: int) -> Response:
    response = requests.delete(
        f"{URL}/friends/delete?friend_id={friend_id}",
        headers={'Authorization': f"Bearer {token['token']}"}
    )
    return response


def accept_invite(req_id: int) -> Response:
    response = requests.post(
        f"{URL}/friend/accept?req_id={req_id}",
        headers={'Authorization': f"Bearer {token['token']}"}
    )
    return response


def get_all_friends_requests() -> Response:
    response = requests.get(
        f"{URL}/friends/all/requests",
    )
    return response


def send_message(receiver_id: int, text: str):
    response = requests.post(
            f"{URL}/messages?receiver_id={receiver_id}&content={text}",

            headers={'Authorization': f"Bearer {token['token']}"}
    )
    return response


def send_new_profile_data(user_data):
    response = requests.put(
        url=f'{URL}/users/update',
        json=user_data,
        headers={'Authorization': f"Bearer {token['token']}"}
    )
    return response


def delete_request(request_id: int):
    response = requests.delete(
        f'{URL}/friends/request?request_id={request_id}',
        headers={'Authorization': f"Bearer {token['token']}"}
    )
    return response


def register(user_data):
    response = requests.post(
        f'{URL}/users/',
        json=user_data
    )
    return response