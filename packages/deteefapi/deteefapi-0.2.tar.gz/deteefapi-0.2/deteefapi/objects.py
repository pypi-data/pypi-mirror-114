from functools import cached_property


class CommentLikes:
    __slots__ = ('_data',)

    def __init__(self, data):
        self._data = data

    def __getitem__(self, item):
        return self._data[item]

    @property
    def is_liked(self) -> int:
        return self['is_liked']

    @property
    def count(self) -> int:
        return self['count']

    @property
    def sum(self) -> int:
        return self['summ']


class Comment:
    __slots__ = ('_data', '__dict__')

    def __init__(self, data):
        """
        {
            'id': 2030289,
            'author': {UserComment},
            'date': 1557740934,
            'dateRFC': 'Mon, 13 May 2019 12:48:54 +0300',
            'isFavorited': False,
            'date_favorite': None,
            'isEdited': False,
            'likes': {CommentLikes},
            'media': [],
            'level': 0,
            'is_pinned': False,
            'is_ignored': False,
            'is_removed': False,
            'replyTo': 0,
            'text': 'И тут Конами присоединилась :О',
            'text_wo_md': 'И тут Конами присоединилась :О',
            'html': '<p>И тут Конами присоединилась :О</p>',
            'attaches': [],
            'source_id': 0,
            'entry': None,
            'load_more': {
                'count': 0,
                'ids': [],
                'avatars': []
            },
            'etcControls': {
                'pin_comment': False,
                'remove': False,
                'remove_thread': False
            },
            'highlight': '',
            'donate': None
        }
        """
        self._data = data

    def __getitem__(self, item):
        return self._data.get(item, None)

    @property
    def id(self) -> int:
        return self['id']

    @cached_property
    def author(self):
        return UserComment(self['author'])

    @property
    def text(self) -> str:
        return self['text']

    @property
    def text_wo_md(self) -> str:
        return self['text_wo_md']

    @property
    def html(self) -> str:
        return self['html']

    @property
    def reply_to(self) -> int:
        return self['replyTo']

    @property
    def date(self) -> int:
        return self['date']

    @property
    def date_rfc(self) -> str:
        return self['dateRFC']

    @property
    def is_favorited(self) -> bool:
        return self['isFavorited']

    @property
    def date_favorite(self):
        return self['date_favorite']

    @property
    def is_edited(self) -> bool:
        return self['isEdited']

    @cached_property
    def likes(self) -> CommentLikes:
        return CommentLikes(self['likes'])


class User:
    __slots__ = ('_data',)

    def __init__(self, data):
        """
            'author':
            {
                'id': 1,
                'name': 'Редакция DTF',
                'type': 1,
                'avatar_url': 'https://...',
                'is_online': False,
                'is_verified': False,
                ...
            }
        """
        self._data = data

    def __getitem__(self, item):
        return self._data.get(item, None)

    @property
    def id(self) -> str:
        return self['id']

    @property
    def name(self) -> str:
        return self['name']

    @property
    def type(self) -> int:
        return self['type']

    @property
    def is_online(self) -> bool:
        return self['is_online']

    @property
    def is_verified(self) -> bool:
        return self['is_verified']

    @property
    def avatar_url(self) -> str:
        return self['avatar_url']


class UserPost(User):
    """
        'avatar': { ... },
        'url': 'https://dtf.ru/u/1',
        'is_subscribed': False
    """

    @property
    def avatar(self) -> dict:
        return self['avatar']

    @property
    def url(self) -> str:
        return self['url']

    @property
    def is_subscribed(self) -> bool:
        return self['is_subscribed']


class UserComment(User):
    @property
    def online_status_text(self) -> str:
        return self['online_status_text']


class Entry:
    __slots__ = ('_data', '__dict__')

    def __init__(self, data):
        self._data = data

    def __getitem__(self, item):
        return self._data[item]

    @property
    def id(self) -> int:
        return self['id']

    @property
    def title(self) -> str:
        return self['title']

    @property
    def entry_content(self) -> dict:
        return self['entryContent']

    @cached_property
    def author(self) -> User:
        return User(self['author'])
