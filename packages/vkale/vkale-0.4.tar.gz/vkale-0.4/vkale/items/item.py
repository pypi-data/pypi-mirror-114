from abc import ABC, abstractmethod


class VKItem:
    __slots__ = ('_data',)

    def __init__(self, data):
        self._data = data

    def __str__(self):
        return f'<{self.__class__.__name__} id:{self.id}>'

    def __repr__(self):
        return self.__str__()

    @property
    def id(self):
        return self.get('id', default_value=None)

    @property
    def date(self):
        return self.get_int('date')

    def __getitem__(self, key):
        return self._data[key]

    def get(self, key, default_value=None):
        return self._data.get(key, default_value)

    def get_string(self, key, default_value=''):
        return self._data.get(key, default_value)

    def get_int(self, key, default_value=0):
        return self._data.get(key, default_value)

    def get_bool(self, key, default_value=False):
        return self._data.get(key, default_value)

    def get_list(self, key, default_value=None):
        if default_value is None:
            default_value = []
        return self._data.get(key, default_value)


class LinkItem(VKItem):
    @property
    def url(self):
        return self.get_string('url')

    @property
    def title(self):
        return self.get_string('title')

    @property
    def description(self):
        return self.get_string('description')


class VKMethodResult(ABC):
    __slots__ = ('_raw', '_data',)

    def __init__(self, data: dict):
        self._raw = data
        self._data = self._handler(data)

    def _handler(self, data):
        return data

    @property
    def response(self) -> dict:
        """May return None"""
        return self._raw.get('response', None)

    def __getitem__(self, key):
        return self._raw[key]


class VKMethodIterableResult(VKMethodResult):
    def __len__(self):
        return len(self._data)

    def __iter__(self):
        for item in self._data:
            yield item

    def _get_item(self, idx: int):
        return self._data[idx]

    @abstractmethod
    def __getitem__(self, idx: int) -> VKItem:
        return self._get_item(idx)
