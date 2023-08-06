from typing import List

from vkale.items import *


class UserItem(VKItem):
    """
    {
        "id": 210700286,
        "first_name": "Lindsey",
        "last_name": "Stirling",
        "is_closed": false,
        "can_access_closed": true,
        "photo_50": "https://sun9-39.u...gaEKflurs&ava=1",
        "verified": 1
    }
    """

    @property
    def id(self) -> int:
        return self.get_int('id')

    @property
    def first_name(self) -> str:
        return self.get_string('first_name')

    @property
    def last_name(self) -> str:
        return self.get_string('last_name')

    @property
    def is_closed(self) -> bool:
        return self.get_bool('is_closed')

    @property
    def can_access_closed(self) -> bool:
        return self.get_bool('can_access_closed')

    @property
    def verified(self) -> int:
        return self.get_int('verified')

    @property
    def photo_50(self) -> str:
        """Url"""
        return self.get_string('photo_50')


class UsersGetResult(VKMethodIterableResult):
    def __getitem__(self, idx: int) -> UserItem:
        return self._get_item(idx)

    def _handler(self, data) -> List[UserItem]:
        return [UserItem(itm) for itm in data['response']]
