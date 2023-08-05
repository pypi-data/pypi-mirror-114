import random
import unittest

from .test_tools import *


class TestBotsInboundProcessor(unittest.TestCase):
    def setUp(self):
        self.bot = get_bot()

    def test_post_many_comments(self):
        messages = ['корова', 'бык', 'локомотив', 'пыль', 'закат', 'револьвер', 'караван', 'покер']
        for i in range(10):
            # response = self.bot.connect()
            msg = random.choice(messages)
            response = self.bot.comment_send(post_id=TEST_POST_ID, text="{} {}".format(msg, i + 1))
            self.assertEqual(response.status_code, 200, response.content)


if __name__ == '__main__':
    unittest.main()
