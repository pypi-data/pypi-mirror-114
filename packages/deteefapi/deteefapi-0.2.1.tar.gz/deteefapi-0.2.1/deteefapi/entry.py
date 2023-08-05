import json
from typing import List, Union

class EntryBlock:
    type = "text"

    def __init__(self, **kwargs):
        self._struct = {
            "type": self.type,
            "data": {},
            "cover": kwargs.get("cover", False),
            "anchor": kwargs.get("anchor", "")
        }

    @property
    def struct(self):
        return self._struct

    @property
    def data(self):
        return self._struct["data"]

    @staticmethod
    def as_url(url, text):
        return '<a href="{}" rel="nofollow noreferrer noopener" target="_blank">{}</a>'.format(url, text)


class EntryPost:
    def __init__(self, title: str = ""):
        self._title = title
        self._struct = {"blocks": []}

    @property
    def json_data(self):
        return json.dumps(self._struct)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, text):
        self._title = text

    @property
    def blocks(self):
        return self._struct["blocks"]

    def add(self, blocks: Union[List[EntryBlock], EntryBlock]):
        if not isinstance(blocks, list):
            blocks = [blocks]
        for block in blocks:
            self.blocks.append(block.struct)


class TextBlockBase(EntryBlock):
    type = "text"

    def __init__(self, text, **kwargs):
        """
        :param text:
        :type text: str | list[str]
        :param kwargs:
        """
        super().__init__(**kwargs)
        if isinstance(text, str):
            self.data["text"] = self.wrap_text(text)
        elif isinstance(text, list):
            self.data["text"] = self.wrap_text_list(text)
        else:
            raise TypeError("text should be str or list[str]: it is {}".format(type(text)))

    def wrap_text(self, text):
        return "<p>{}</p>".format(text)

    def wrap_text_list(self, text_list):
        return "".join([self.wrap_text(text) for text in text_list])

    def add_text(self, text):
        self.data["text"] += self.wrap_text(text)


class TextBlock(TextBlockBase):
    def __init__(self, text, **kwargs):
        super().__init__(text, **kwargs)
        self.data["text_truncated"] = "<<<same>>>"


class HeaderBlock(TextBlockBase):
    type = "header"

    def __init__(self, text, header_style=2, **kwargs):
        super().__init__(text, **kwargs)
        self.data["style"] = "h{}".format(header_style)


class IncutBlock(TextBlockBase):
    type = "incut"

    def __init__(self, text, type='left', text_size='small', **kwargs):
        super().__init__(text, **kwargs)
        self.data["type"] = type  # left/centered
        self.data["text_size"] = text_size  # big/small


class MediaBlock(EntryBlock):
    type = "media"

    def __init__(self, image_data, **kwargs):
        super().__init__(**kwargs)
        self._struct["data"] = {
            "items": [{
                "title": kwargs.get("title", ""),
                "author": kwargs.get("author", ""),
                "image": image_data
            }
            ],
            "with_background": kwargs.get("with_background", False),
            "with_border": kwargs.get("with_border", False)
        }
