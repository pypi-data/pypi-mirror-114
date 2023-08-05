import unittest

from deteefapi import serialize_webhook_data
from .test_tools import *


class TestGetData(unittest.TestCase):
    def setUp(self):
        self.bot = get_bot()

    def test_dtf_comment(self):
        response = self.bot.connect()
        self.assertEqual(response.status_code, 200, response.content)

    def test_get_comment(self):
        # 1
        comment = self.bot.get_comment_by_id(entry_id=1, comment_id=1)
        self.assertTrue('Буду первым' in comment.text, msg=comment.text)
        self.assertEqual(comment.author.name, 'Ilya Suragin', msg=comment.author._data)
        self.assertEqual(comment.author.id, 12, msg=comment.author._data)
        # 2
        comment = self.bot.get_comment_by_id(entry_id=1, comment_id=2)
        self.assertTrue('Поздравляю!' in comment.text, msg=comment.text)
        self.assertEqual(comment.author.name, 'Sergey Kopov', msg=comment.author._data)
        self.assertEqual(comment.author.id, 21, msg=comment.author._data)

    def test_get_user_comments(self):
        comments = self.bot.get_user_comments(user_id=TEST_BOT_ID, count=10, offset=0)
        count = 0
        for comment in comments:
            with self.subTest(comment=comment):
                self.assertEqual(comment.author.id, TEST_BOT_ID, msg=comment)
            count += 1
        self.assertEqual(count, 10, msg='Wrong number of comments')

    def test_get_entry(self):
        # get entry
        response = self.bot.get_entry(post_id=1)
        data = response.json()
        title = data['result']['title']
        self.assertTrue('Никогда такого не было – и снова DTF' in title, msg=data)

    def test_webhook_data(self):
        comment = serialize_webhook_data(TEST_WEBHOOK_DATA)
        self.assertEqual(2102074, comment.id, comment._data)
        self.assertEqual(84125, comment.content.id, comment._data)
        self.assertEqual(2102073, comment.reply_to.id, comment._data)
        self.assertEqual(1, comment.reply_to.creator.id, comment._data)


if __name__ == '__main__':
    unittest.main()
