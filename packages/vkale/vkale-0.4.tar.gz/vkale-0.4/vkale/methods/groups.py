from typing import Union

from vkale.items.callback import *
from vkale.method import *


class Groups(VKMethodGroup):
    _name = 'groups'

    def __init__(self, vk_api):
        super().__init__(vk_api)
        self.get_callback_servers = GetCallbackServers(self)
        self.get_callback_settings = GetCallbackSettings(self)
        self.set_callback_settings = SetCallbackSettings(self)
        self.add_callback_server = AddCallbackServer(self)
        self.delete_callback_server = DeleteCallbackServer(self)

    def get_callback_server_by_name(self, group_id: int, server_name: str) -> Union[VKCallbackServer, None]:
        servers = self.get_callback_servers(group_id=group_id)
        for server in servers:
            if server.title == server_name:
                return server
        return None

    def delete_callback_server_by_name(self, group_id: int, server_name: str) -> int:
        server = self.get_callback_server_by_name(group_id=group_id, server_name=server_name)
        if server:
            return self.delete_callback_server(group_id=group_id, server_id=server.id)
        return 0


class GetCallbackSettings(VKMethod):
    _name = 'getCallbackSettings'
    _result_handler = GetCallbackSettingsResult

    def __call__(self, group_id, server_id) -> GetCallbackSettingsResult:
        return self.request(dict(group_id=group_id, server_id=server_id))


class SetCallbackSettings(VKMethod):
    _name = 'setCallbackSettings'

    def __call__(self, group_id: int, server_id: int, **params) -> int:
        """
        :param group_id: positive number
        :param server_id:
        :return:
        """
        response = self.request(dict(group_id=group_id, server_id=server_id, **params))
        return response.response


class AddCallbackServer(VKMethod):
    _name = 'addCallbackServer'

    def __call__(self, group_id: int, title: str, url: str, secret_key: str = None) -> int:
        """Returns server_id"""
        params = dict(group_id=group_id, title=title, url=url)
        if secret_key:
            params['secret_key'] = secret_key
        response = self.request(params)
        return response.response


class DeleteCallbackServer(VKMethod):
    _name = 'deleteCallbackServer'

    def __call__(self, group_id: int, server_id: int) -> int:
        """
        :param group_id: positive number
        :param server_id:
        :return:
        """
        response = self.request(dict(group_id=group_id, server_id=server_id))
        return response.response


class GetCallbackServers(VKMethod):
    _name = 'getCallbackServers'
    _result_handler = GetCallbackServersResult

    def __call__(self, group_id, servers_id: List[int] = None) -> GetCallbackServersResult:
        params = {'group_id': group_id}
        if servers_id:
            params['servers_id'] = ','.join(map(str, servers_id))
        return self.request(params)
