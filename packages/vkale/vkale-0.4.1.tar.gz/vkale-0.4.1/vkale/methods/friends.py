from vkale.items.friends_items import *
from vkale.method import *


class Friends(VKMethodGroup):
    _name = 'friends'

    def __init__(self, vk_api):
        super().__init__(vk_api)
        self.get = Get(self)


class Get(VKMethod):
    _name = 'get'
    _result_handler = FriendsGetResult

    def __call__(self, user_id, count, offset=0, order='hints', **kwargs) -> FriendsGetResult:
        return self.request(dict(user_id=user_id, count=count, offset=offset))
