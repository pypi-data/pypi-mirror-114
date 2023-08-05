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

TEST_WEBHOOK_DATA = {
    "type": "new_comment",
    "data":
        {
            "id": 2102074,
            "url": "https://tjournal.ru\/art\/84125-na-noch-glyadya?comment=2102074",
            "text": "А это ответ",
            "media": [

            ],
            "creator": {
                "id": 1,
                "avatar": "https://leonardo.osnova.io\/d49d71ab-f78a-db1d-b4c4-0c72b8fcda0e\/",
                "name": "Ilya Chekalsky",
                "url": "https://tjournal.ru\/u\/1-ilya-chekalsky"
            },
            "content": {
                "id": 84125,
                "title": "На ночь глядя",
                "url": "https://tjournal.ru\/art\/84125-na-noch-glyadya",
                "owner": {
                    "id": 214363,
                    "name": "Арт и дизайн",
                    "avatar": "https://leonardo.osnova.io\/357dedc0-c17e-2e05-e568-b7c383257091\/",
                    "url": "https://tjournal.ru\/art"
                }
            },
            "reply_to": {
                "id": 2102073,
                "url": "https://tjournal.ru\/art\/84125-na-noch-glyadya?comment=2102073",
                "text": "Это родительский комментарий",
                "media": [

                ],
                "creator": {
                    "id": 1,
                    "avatar": "https://leonardo.osnova.io\/d49d71ab-f78a-db1d-b4c4-0c72b8fcda0e\/",
                    "name": "Ilya Chekalsky",
                    "url": "https://tjournal.ru\/u\/1-ilya-chekalsky"
                }
            }
        }
}


def get_bot():
    return DeteefAPI(DTF_CONFIG['token'])


class DTF_API_FAKE(DeteefAPI):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass
