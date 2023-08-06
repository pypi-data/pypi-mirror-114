from .lib.objects import *
from .lib.exceptions import *
from .threads import Threads

import threading
import random

import requests
import json


class Client(Threads):
    def __init__(self, session_id: int = str(random.randint(1, 9999))):
        self.token = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "session-id": session_id,
            "x-user-agent": "14 Web/1 ru"
        }
        self.api = 'https://capture.chat/api'
        Threads.__init__(self)

    def login_token(self, token: str):
        self.headers["X-Token"] = token

    def get_topic_messages(self, topicId: str, count: int = 10):
        data = json.dumps({})
        url = f'{self.api}/topic/{topicId}/message?count={count}'
        response = requests.get(url, data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return MessageList(response.json()["items"]).MessageList

    def send_message(self, topicId: str, message: str, replyMessage: str = None):
        data = {
            'text': message
        }

        if replyMessage is None: pass
        else: data["quote_message_id"] = replyMessage
        url = f'{self.api}/topic/{topicId}/message'
        data = json.dumps(data)
        response = requests.post(url, headers=self.headers, data=data)
        if response.status_code != 200: return CheckExceptions(response.json())
        else: return Message(response.json()).Message

    def create_topic(self, bio: str, name: str, ischannel: bool = False, isprivate: bool = False):
        data = json.dumps({
            'channel': ischannel,
            'private': isprivate,
            'name': name,
            'content': bio
        })
        url = f'{self.api}/topic'
        response = requests.post(url, data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def edit_topic(self, topicId: str, bio: str = None, name: str = None, categoryId: int = 1):
        data = json.dumps({
            'category_id': categoryId,
            'name': name,
            'discription': bio
        })
        url = f'{self.api}/topicId{topicId}'
        response = requests.patch(url, data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def get_topic_id(self, url: str):
        """
            Get topic ID from url.
            **Parameters**

        - **url** : url of the topic
"""
        url = f'{self.api}/link/preview?url={url}'
        response = requests.get(url)
        topic_id = str(response.json()['topic_id'])
        if response.status_code != 200: CheckExceptions(response.json())
        else: return topic_id

    def login(self, email: str):
        url = f'{self.api}/auth/?username={email}%40gmail.com'
        response = requests.post(url)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def delete_message(self, topicId: str, messageId: str):
        url = f'{self.api}/topic/{topicId}/message{messageId}'
        response = requests.delete(url, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def get_notifications(self):
        url = f'{self.api}/notification'
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return Notifications(response.json()["items"]).Notifications

    def get_topic_users(self, topicId: str, count: int = 10):
        url = f'{self.api}/topic/{topicId}/member?count={count}'
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return UserProfileList(response.json()["items"]).UserProfileList

    def get_user_topics(self, userId: str, count: int = 10):
        url = f'{self.api}/user/{userId}/topic?count={count}'
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return TopicList(response.json()["items"]).TopicList

    def get_discover_topic(self, needMembers: bool = False, count: int = 10):
        url = f'{self.api}/topic/discover?count={count}&need_members= + {needMembers}'
        response = requests.get(url)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return TopicList(response.json()["items"]).TopicList

    def leave_topic(self, topicId: str):
        url = f'{self.api}/topic/{topicId}/subscription'
        response = requests.delete(url, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def join_topic(self, topicId: str):
        url = f'{self.api}/topic/{topicId}/subscription'
        response = requests.post(url, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def edit_profile(self, photo: str = None, username: str = None, bio: str = None, location: str = None, status: bool = True):
        data = json.dumps({
            'bio': bio,
            'location': location,
            'name': username,
            'online': status,
            'photo': photo
        })
        url = f'{self.api}/user/me'
        response = requests.patch(url, data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def sign_up(self, username):
        data = json.dumps({
            'username': username
        })
        url = f'{self.api}/auth/username'
        response = requests.post(url, data=data)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return NewAcc(response.json()).NewAcc

    def change_user_role(self, topicId: str, userId: str, role: str):
        data = json.dumps({
            'admin': role
        })
        url = f'{self.api}/topic/{topicId}/member/{userId}'
        response = requests.patch(url, data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def edit_message(self, topicId: str, messageId: str, newText: str):
        data = json.dumps({
            'text': newText
        })
        url = f'{self.api}/topic/{topicId}/message/{messageId}'
        response = requests.patch(url, data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def ban(self, topicId: str, userId: str):
        url = f'{self.api}/topic/{topicId}/ban{userId}'
        response = requests.post(url, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def report(self, userId: str, reason: str = 'From Web'):
        data = {
            'reason': reason
        }
        if reason is None: data['comment'] = 'Web'
        data = json.dumps(data)
        url = f'{self.api}/user/{userId}/report'
        response = requests.post(url, data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def report_message(self, topicId: str, messageId: str, reason: str = 'From Web'):
        data = {
            'reason': reason
        }
        if reason is None: data['comment'] = 'Web'
        data = json.dumps(data)
        url = f'{self.api}/topic/{topicId}/message/{messageId}'
        response = requests.post(url, data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def unban(self, topicId: str, userId: str):
        url = f'{self.api}/topic/{topicId}/ban{userId}'
        response = requests.delete(url, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def start_dm(self, userId: str):
        url = f'{self.api}/dm/user/{userId}'
        response = requests.post(url, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def get_topics(self, count: int = 10, messageLimit: int = 0, returnAll: bool = False):
        url = f'{self.api}/topic?count={count}&messages_limit{messageLimit}&return_all={returnAll}'
        response = requests.get(url, headers=self.headers)
        response = json.loads(response.text)
        return TopicList(response["items"]).TopicList

    def follow(self, topicId: str):
        url = f'{self.api}/topic/{topicId}/follow'
        response = requests.post(url, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def unfollow(self, topicId: str):
        url = f'{self.api}/topic/{topicId}/unfollow'
        response = requests.delete(url, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def start_typing_status(self, topicId: str, messageId: str = None, time: int = 5, status: str = "text"):
        threading.Thread(target=self.send, args=(self._send_typing_status_, (self.headers, topicId, status, ), time)).start()
        if messageId is None: pass
        else: threading.Thread(target=self.send_edit, args=(self._when_typing_, topicId, messageId, )).start()
