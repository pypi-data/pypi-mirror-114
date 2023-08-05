from typing import Generator

import requests
from backoff import on_exception, expo
from ratelimit import limits, sleep_and_retry, RateLimitException

from .entry import *
from .objects import *
from .webhook import WebhookData


class DeteefAPI:
    _API_VER = '1.9'
    __slots__ = ('_token', '_api_url', '_session')

    def __init__(self, token):
        self._token = token
        self._api_url = f'https://api.dtf.ru/v{self._API_VER}/'
        self._session = requests.session()
        self._session.headers.update({'X-Device-Token': self._token})

    def api_url(self, sub_path):
        return self._api_url + sub_path

    def get(self, *args, **kwargs) -> requests.Response:
        return self._request('get', *args, **kwargs)

    @sleep_and_retry
    @limits(calls=1, period=1.3)
    def post(self, *args, **kwargs) -> requests.Response:
        return self._request('post', *args, **kwargs)

    @sleep_and_retry
    @on_exception(expo, RateLimitException, max_tries=8, max_time=60)
    @limits(calls=3, period=1.5)
    def _request(self, req_type, *args, **kwargs) -> requests.Response:
        if req_type == 'get':
            response = self._session.get(*args, **kwargs)
        elif req_type == 'post':
            response = self._session.post(*args, **kwargs)
        else:
            response = None
        if response.status_code != 200:
            if response.status_code == 400 and response.json().get("message",
                                                                   "") == "Повторная отправка того же сообщения":
                return response
            raise Exception(f'API response: {response.status_code}; msg: {response.text}')
        return response

    def connect(self):
        url = self.api_url('user/me')
        return self.get(url=url)

    # api methods
    def get_user(self, user_id):
        url = self.api_url(f'user/{user_id}')
        response = self.get(url=url)
        return response

    def get_entry(self, post_id):
        url = self.api_url(f'entry/{post_id}')
        response = self.get(url=url)
        return response

    def create_entry_simple(self, title, text, subsite_id, attachments=None):
        url = self.api_url('entry/create')
        response = self.post(url=url,
                             data=dict(title=title, text=text, subsite_id=subsite_id, attachments=attachments or {}))
        return response

    def create_entry(self, entry: EntryPost, subsite_id: int, title: str = None, attachments=None) -> Entry:
        url = self.api_url("entry/create")
        entry.title = entry.title or title
        attachments = attachments or {}
        response = self.post(url=url, data=dict(title=entry.title,
                                                entry=entry.json_data,
                                                subsite_id=subsite_id,
                                                attachments=attachments))
        data = response.json() or {}
        return Entry(data.get('result', {}))

    def get_entry_comments_thread(self, entry_id, comment_id):
        url = self.api_url(f'entry/{entry_id}/comments/thread/{comment_id}')
        response = self.get(url=url)
        data = response.json()
        return data

    def comment_send(self, post_id, text, reply_to=0, attachments=None) -> requests.Response:
        url = self.api_url("comment/add")
        response = self.post(url=url,
                             data=dict(id=post_id, text=text, reply_to=reply_to, attachments=attachments or {}))
        return response

    def get_user_comments(self, user_id, count, offset) -> Generator[Comment, None, None]:
        url = self.api_url(f'user/{user_id}/comments')
        response = self.get(url=url, params=dict(count=count, offset=offset))
        data = response.json() or {}
        items = data.get('result')
        return (Comment(item) for item in items)

    # workarounds
    def get_comment_by_id(self, entry_id, comment_id) -> Comment:
        data = self.get_entry_comments_thread(entry_id, comment_id)
        for comment_data in data["result"]["items"]:
            if comment_data["id"] == comment_id:
                return Comment(comment_data)
        return Comment(None)

    # attachments
    def upload(self, media_url, get_index=0):
        url = self.api_url('uploader/extract')
        response = self.post(url=url, data=dict(url=media_url))
        data = response.json().get("result", [{}])
        return data[get_index]

    @staticmethod
    def get_user_url(user_id, name):
        return f'[@{user_id}|{name}]'

    def get_webhook(self) -> WebhookData:
        url = self.api_url('webhooks/get')
        response = self.get(url)
        return WebhookData(response.json().get('result', {}))

    def set_webhook(self, webhook_url: str, event: str = 'new_comment', secret_code: str = None) -> requests.Response:
        url = self.api_url('webhooks/add')
        data = {'url': webhook_url, 'event': event}
        if secret_code:
            data['secret_code'] = secret_code
        response = self.post(url, data=data)
        return response

    def delete_webhook(self, webhook_url: str, event: str = 'new_comment') -> requests.Response:
        url = self.api_url('webhooks/del')
        data = {'url': webhook_url, 'event': event}
        response = self.post(url, data=data)
        return response
