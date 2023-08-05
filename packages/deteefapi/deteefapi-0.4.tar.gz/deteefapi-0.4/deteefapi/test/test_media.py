import unittest

from deteefapi.entry import EntryPost, MediaBlock
from .test_tools import *


class TestBotsInboundProcessor(unittest.TestCase):
    def setUp(self):
        self.bot = get_bot()

    def test_dtf_entry_media(self):
        image_data = self.bot.upload(media_url="http://www.metta.org.uk/travel/images/caravan.jpg")
        self.assertEqual(image_data['type'], 'image', image_data)
        self.assertEqual(image_data['data']['uuid'], '541d2a04-5e59-5d1c-9453-1ca407ec9d22', image_data)
        entry = EntryPost()
        entry.add(MediaBlock(image_data=image_data, cover=True))

        title = 'post_with_url_media'
        response_entry = self.bot.create_entry(entry, subsite_id=TEST_SUBSITE_ID, title=title)
        self.assertEqual(response_entry.title, title, response_entry._data)


if __name__ == '__main__':
    unittest.main()
