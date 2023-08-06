from typing import Union

from vkale.items.user_items import *
from vkale.method import *


class Users(VKMethodGroup):
    __slots__ = ('get',)
    _name = 'users'

    def __init__(self, vk_api):
        super().__init__(vk_api)
        self.get = Get(self)


class Get(VKMethod):
    _name = 'get'
    _result_handler = UsersGetResult

    def __call__(self, user_ids: Union[str, list],
                 fields: Union[str, list] = None,
                 name_case: str = None,
                 **kwargs) -> UsersGetResult:
        """fields: photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig,
        photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education,
        universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives,
        relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about,
        quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request,
        is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status,
        career, military, blacklisted, blacklisted_by_me, can_be_invited_group.

        именительный – nom, родительный – gen, дательный – dat, винительный – acc, творительный – ins, предложный – abl
        """
        if isinstance(user_ids, list):
            user_ids = ','.join(user_ids)
        params = dict(user_ids=user_ids)

        if fields is not None:
            if isinstance(fields, list):
                fields = ','.join(fields)
            params['fields'] = fields

        if name_case is not None:
            params['name_case'] = name_case
        return self.request(params)
