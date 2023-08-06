from vkale.items.wall_items import *
from vkale.method import *


class Wall(VKMethodGroup):
    __slots__ = ('get', 'post')
    _name = 'wall'

    def __init__(self, vk_api):
        super().__init__(vk_api)
        self.get = Get(self)
        self.post = Post(self)


class Get(VKMethod):
    _name = 'get'
    _result_handler = WallGetResult

    def __call__(self, owner_id, count, offset=0, **kwargs) -> WallGetResult:
        return self.request(dict(owner_id=owner_id, count=count, offset=offset))


class Post(VKMethod):
    _name = 'post'

    def __call__(self, message: str, owner_id: int, from_group, **kwargs) -> dict:
        """
        :param message:
        :param owner_id: Negative if group
        :param from_group:
        :param kwargs:
        :return:
        """
        return self.request(dict(message=message, owner_id=owner_id, from_group=from_group))
