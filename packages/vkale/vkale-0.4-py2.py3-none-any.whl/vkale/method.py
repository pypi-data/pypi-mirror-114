from .common import API_METHOD_URL
from .items.item import VKMethodResult


class VKMethodGroup:
    __slots__ = ('_vk', 'method_group_url')
    _name: str = None

    def __init__(self, vk_api):
        self._vk = vk_api
        if self._name is None:
            raise Exception(f'{self.__class__.__name__} has no name')
        self.method_group_url = f'{API_METHOD_URL}/{self._name}'

    def request(self, method_url: str, params):
        return self._vk.request(method_url, params)

    def __call__(self, method_name: str, **params):
        method_url = f'{self.method_group_url}.{method_name}'
        return self._vk.request(method_url, params)


class VKMethod:
    __slots__ = ('_method_group', 'method_url')
    _name: str = None
    _result_handler = VKMethodResult

    def __init__(self, vk_method_group: VKMethodGroup):
        self._method_group = vk_method_group
        if self._name is None:
            raise Exception(f'{self.__class__.__name__} has no name')
        self.method_url: str = f'{self._method_group.method_group_url}.{self._name}'

    def request(self, params):
        return self._result_handler(self._method_group.request(self.method_url, params))
