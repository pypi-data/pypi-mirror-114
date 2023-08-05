from __future__ import annotations

import json
from collections import defaultdict
from functools import cached_property
from typing import Union, Generator, Dict, List


class CommentCreator:
    def __init__(self, data):
        """
        {
            "id": 1,
            "avatar": "https://leonardo.osnova.io/d49d71ab-f78a-db1d-b4c4-0c72b8fcda0e/",
            "name": "Ilya Chekalsky",
            "url": "https://tjournal.ru/u/1-ilya-chekalsky"
        }
        """
        self._data = data

    @property
    def id(self) -> int:
        return self._data['id']

    @property
    def name(self) -> str:
        return self._data['name']

    @property
    def avatar(self) -> str:
        return self._data['avatar']

    @property
    def url(self) -> str:
        return self._data['url']


class CommentEntrySubsite:
    def __init__(self, data):
        """ "owner":
        {
            "id": 214363,
            "name": "Арт и дизайн",
            "avatar": "https://leonardo.osnova.io/357dedc0-c17e-2e05-e568-b7c383257091/",
            "url": "https://tjournal.ru/art"
        }
        """
        self._data = data

    @property
    def id(self) -> int:
        return self._data['id']

    @property
    def title(self) -> str:
        return self._data['title']

    @property
    def url(self) -> str:
        return self._data['url']


class CommentEntry:
    __slots__ = ('_data', '_owner')

    def __init__(self, data):
        """
        {
            "id": 84125,
            "title": "На ночь глядя",
            "url": "https://tjournal.ru/art/84125-na-noch-glyadya",
            "owner": {
                "id": 214363,
                "name": "Арт и дизайн",
                "avatar": "https://leonardo.osnova.io/357dedc0-c17e-2e05-e568-b7c383257091/",
                "url": "https://tjournal.ru/art"
            }
        }
        """
        self._data = data
        self._owner = CommentEntrySubsite(self._data['owner'])

    @property
    def id(self) -> int:
        return self._data['id']

    @property
    def title(self) -> str:
        return self._data['title']

    @property
    def url(self) -> str:
        return self._data['url']

    @property
    def owner(self) -> CommentEntrySubsite:
        return self._owner


class WebhookComment:
    __slots__ = ('_data', '__dict__')

    def __init__(self, data):
        """
        {
            "type": "new_comment",
            "data": {
                "id": 2102074,
                "url": "https://tjournal.ru/art/84125-na-noch-glyadya?comment=2102074",
                "text": "А это ответ",
                "media": [],
                "creator": {
                    "id": 1,
                    "avatar": "https://leonardo.osnova.io/d49d71ab-f78a-db1d-b4c4-0c72b8fcda0e/",
                    "name": "Ilya Chekalsky",
                    "url": "https://tjournal.ru/u/1-ilya-chekalsky"
                },
                "content": {
                    "id": 84125,
                    "title": "На ночь глядя",
                    "url": "https://tjournal.ru/art/84125-na-noch-glyadya",
                    "owner": {
                        "id": 214363,
                        "name": "Арт и дизайн",
                        "avatar": "https://leonardo.osnova.io/357dedc0-c17e-2e05-e568-b7c383257091/",
                        "url": "https://tjournal.ru/art"
                    }
                },
                "reply_to": {
                    "id": 2102073,
                    "url": "https://tjournal.ru/art/84125-na-noch-glyadya?comment=2102073",
                    "text": "Это родительский комментарий",
                    "media": [
        
                    ],
                    "creator": {
                        "id": 1,
                        "avatar": "https://leonardo.osnova.io/d49d71ab-f78a-db1d-b4c4-0c72b8fcda0e/",
                        "name": "Ilya Chekalsky",
                        "url": "https://tjournal.ru/u/1-ilya-chekalsky"
                    }
                }
            }
        }
        """
        self._data = data

    def __getitem__(self, item):
        return self._data[item]

    @property
    def id(self) -> int:
        return self['id']

    @property
    def text(self) -> str:
        return self['text']

    @cached_property
    def reply_to(self) -> WebhookComment:
        return WebhookComment(self._data.get("reply_to", {}))

    @property
    def reply_to_full_id(self):
        return f'{self.content.id}_{self.reply_to.id}'

    @property
    def full_id(self):
        return f'{self.content.id}_{self.id}'

    @cached_property
    def creator(self) -> CommentCreator:
        return CommentCreator(self['creator'])

    @cached_property
    def content(self) -> CommentEntry:
        return CommentEntry(self['content'])

    @property
    def subsite_id(self) -> int:
        return self.content.owner.id


def serialize_webhook_data(webhook_data: Union[dict, str]) -> Union[WebhookComment, None]:
    if isinstance(webhook_data, str):
        webhook_data = json.loads(webhook_data)
    if webhook_data['type'] != 'new_comment':
        return None
    return WebhookComment(webhook_data['data'])


class WebhookData:
    def __init__(self, data: list):
        """
        [
            {
            "id": 39972,
            "event": "new_comment",
            "url": "https://example.com/webhooks/new_com?token=7712md2md4up82"
            }
        ]
        """
        self._data = data
        self._urls_events = defaultdict(set)
        for item in self:
            self._urls_events[item['url']].add(item['event'])

    def __iter__(self) -> Generator[dict, None, None]:
        return (item for item in self._data)

    @property
    def urls_events(self) -> Dict[str, set]:
        return self._urls_events

    def get_url(self, index=0) -> str:
        if self.urls:
            return self.urls[index]
        return ''

    @property
    def urls(self) -> List[str]:
        return list(self.urls_events.keys())

    def is_webhook(self, webhook_url, event_type='new_comment') -> bool:
        return webhook_url in self._urls_events and event_type in self._urls_events[webhook_url]
