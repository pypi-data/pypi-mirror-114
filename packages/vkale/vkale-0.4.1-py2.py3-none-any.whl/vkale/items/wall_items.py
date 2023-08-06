import datetime

from vkale.items import *


class WallItem(VKItem):
    @property
    def id(self):
        return self.get_int('id')

    @property
    def text(self):
        return self.get_string('text')

    @property
    def from_id(self) -> int:
        return self.get_int('from_id')

    @property
    def date_day(self):
        return datetime.datetime.fromtimestamp(self.date).date()

    @property
    def attachments(self):
        return self.get_list('attachments')

    @property
    def links(self):
        return [LinkItem(attachment['link']) for attachment in self.attachments if attachment['type'] == 'link']

    @property
    def link_texts(self):
        return '\n'.join(link.title + '\n' + link.description for link in self.links)

    @property
    def is_pinned(self):
        return self.get_int('is_pinned')


class WallGetResult(VKMethodIterableResult):
    def _handler(self, data):
        return [WallItem(item) for item in data['response']['items']]

    def __getitem__(self, idx: int) -> WallItem:
        return self._get_item(idx)
