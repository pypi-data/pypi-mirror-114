from typing import Generator, List

from vkale.items import *


class VKCallbackServer(VKItem):
    """{'id': 0, 'title': 'main', 'creator_id': 100, 'url': 'https://url.ru', 'secret_key': '', 'status': 'ok'}"""

    def is_empty(self):
        return self._data is None

    @property
    def id(self) -> int:
        return self._data.get('id', None)

    @property
    def title(self) -> str:
        return self._data.get('title', None)

    @property
    def creator_id(self) -> int:
        return self._data.get('creator_id', None)

    @property
    def url(self) -> str:
        return self._data.get('url', None)

    @property
    def secret_key(self) -> str:
        return self._data.get('secret_key', None)

    @property
    def status(self) -> str:
        return self._data.get('status', None)


class GetCallbackServersResult(VKMethodIterableResult):
    def __getitem__(self, idx: int) -> VKCallbackServer:
        return self._get_item(idx)

    def _handler(self, data) -> List[VKCallbackServer]:
        if self.response:
            return [VKCallbackServer(item) for item in self.response.get('items', [])]
        return []

    def __iter__(self) -> Generator[VKCallbackServer, None, None]:
        for item in self._data:
            yield item


class GetCallbackSettingsResult(VKMethodResult):
    @property
    def events(self):
        return self['events']

    @property
    def message_new(self):
        return self.events['message_new']
