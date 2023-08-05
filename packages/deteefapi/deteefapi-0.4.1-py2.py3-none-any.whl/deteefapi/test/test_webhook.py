import unittest

from .test_tools import *


class TestComment(unittest.TestCase):
    def setUp(self):
        self.bot = get_bot()

    def test_dtf_set_webhook(self):
        # set webhook
        webhook_url = DTF_CONFIG['webhook_url']

        response = self.bot.set_webhook(webhook_url=DTF_CONFIG['webhook_url'])
        response_json = response.json()
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response_json['result']['url'], DTF_CONFIG['webhook_url'], response_json)

        # ensure there is webhook: get webhook
        webhook_data = self.bot.get_webhook()
        self.assertTrue(webhook_data.is_webhook(webhook_url, event_type='new_comment'), webhook_data._data)
        self.assertEqual(webhook_data.get_url(), webhook_url, webhook_data._data)

        # set webhook
        response = self.bot.delete_webhook(webhook_url=DTF_CONFIG['webhook_url'])
        response_json = response.json()
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response_json['result']['success'], True, response_json)

        # ensure there is no webhook: get removed webhook
        webhook_data = self.bot.get_webhook()
        self.assertFalse(webhook_data.is_webhook(webhook_url, event_type='new_comment'), webhook_data._data)


if __name__ == '__main__':
    unittest.main()
