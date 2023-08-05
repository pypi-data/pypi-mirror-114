import json
import os

from deteefapi.dtf import DeteefAPI

_CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(_CUR_DIR, 'data')

with open(os.path.join(DATA_DIR, 'dtf.json'), 'r', encoding='utf-8') as f:
    DTF_CONFIG = json.load(f)

TEST_POST_ID = DTF_CONFIG['test_post_id']
TEST_BOT_ID = DTF_CONFIG['bot_id']
TEST_SUBSITE_ID = 130721


def get_bot():
    return DeteefAPI(DTF_CONFIG['token'])


class DTF_API_FAKE(DeteefAPI):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass
