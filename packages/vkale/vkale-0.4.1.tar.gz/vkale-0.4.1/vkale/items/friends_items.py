from typing import List

from vkale.items import *


class FriendsGetResult(VKMethodResult):
    @property
    def count(self):
        return self.response['count']

    @property
    def items(self) -> List[int]:
        return self.response['items']
