import json
import os

from vkale import VKaleAPI

_CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(_CUR_DIR, 'apidata')


def api_data(subpath):
    return os.path.join(DATA_DIR, subpath)


with open(api_data('vkdata.json'), 'r', encoding='utf-8') as f:
    _TEST_DATA = json.load(f)

TEST_GROUP_ID_NEG = _TEST_DATA['TEST_GROUP_ID_NEG']
TEST_GROUP_ID_POS = _TEST_DATA['TEST_GROUP_ID_POS']
TEST_USER_ID = _TEST_DATA['TEST_USER_ID']
TEST_WEBHOOK_URL = _TEST_DATA['TEST_WEBHOOK_URL']


def get_bot() -> VKaleAPI:
    return VKaleAPI(api_base_data_path=api_data("vk_api_bot.json"), is_group_key=True)


def get_api() -> VKaleAPI:
    return VKaleAPI(api_base_data_path=api_data("vk_api.json"))
