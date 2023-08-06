import json
import logging

import requests
from ratelimit import limits, sleep_and_retry

from vkale.methods import *
from .common import API_METHOD_URL

_VKALE_VK_VER_DEFAULT = '5.131'

_REQUEST_RATE_DEFAULT_PARAMS = {'period': 1.5, 'calls': 3}
_REQUEST_RATE_DEFAULT_GROUP_PARAMS = {'period': 1.5, 'calls': 20}

'''
URL EXAMPLE: https://api.vk.com/method/METHOD_NAME?PARAMETERS&access_token=ACCESS_TOKEN&v=V
'''

logger = logging.getLogger('vkale')
logger.addHandler(logging.NullHandler())


class VKaleAPI:
    __slots__ = (
        '_session',
        '_request_rate_params',
        'api_ver',
        'api_base_params',
        'wall',
        'friends',
        'groups',
        'users',
        'messages'
    )

    def __init__(self, token=None, api_ver=None, api_base_data_path=None, is_group_key=False):
        self._session = requests.session()
        self.api_ver = api_ver
        self.api_base_params = {'access_token': token, 'v': self.api_ver if self.api_ver else _VKALE_VK_VER_DEFAULT}
        if api_base_data_path:
            with open(api_base_data_path, 'r', encoding='utf-8') as f:
                self.api_base_params = json.load(f)

        if is_group_key:
            self._request_rate_params = _REQUEST_RATE_DEFAULT_GROUP_PARAMS
        else:
            self._request_rate_params = _REQUEST_RATE_DEFAULT_PARAMS

        # region Method Groups
        self.wall = Wall(self)
        self.friends = Friends(self)
        self.groups = Groups(self)
        self.users = Users(self)
        self.messages = Messages(self)
        # endregion

    def method(self, method_name, **kwargs):
        return self.request(f'{API_METHOD_URL}/{method_name}', kwargs)

    def request(self, method_url, params: dict = None) -> dict:
        @sleep_and_retry
        @limits(**self._request_rate_params)
        def _request():
            return self._session.get(method_url, params=params)

        if params is None:
            params = self.api_base_params.copy()
        else:
            params.update(self.api_base_params)
        response = _request()
        response = response.json()
        logger.info(f"vkale request: {response}")
        return response


if __name__ == '__main__':
    pass
