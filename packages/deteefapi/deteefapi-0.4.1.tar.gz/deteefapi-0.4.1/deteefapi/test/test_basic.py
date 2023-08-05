import random
import unittest

from deteefapi.entry import EntryPost, TextBlock
from .test_tools import *


class TestComment(unittest.TestCase):
    def setUp(self):
        self.bot = get_bot()

    def test_dtf_comment(self):
        seed = random.randint(1, 10000000)
        test_text = 'u_test'
        response = self.bot.comment_send(post_id=TEST_POST_ID, text=f'{test_text} {seed}', reply_to=0)
        self.assertEqual(response.status_code, 200, response.content)
        data = response.json()
        text = data['result']['text']
        self.assertTrue(test_text in text, msg=data)

    def test_dtf_entry(self):
        title = "test_title"
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n" \
               "Phasellus feugiat felis tincidunt tortor consequat, eget tincidunt diam maximus."
        # form entry
        entry = EntryPost(title=title)
        entry.add(TextBlock(text, cover=True))
        # post
        response_entry = self.bot.create_entry(entry=entry, subsite_id=TEST_SUBSITE_ID)
        self.assertEqual(response_entry.title, title, response_entry._data)
        # comment on post
        test_text = 'test post comment'
        response = self.bot.comment_send(post_id=response_entry.id, text=test_text, reply_to=0)
        self.assertEqual(response.status_code, 200, response.content)
        # delete post
        # TODO: delete


if __name__ == '__main__':
    unittest.main()
