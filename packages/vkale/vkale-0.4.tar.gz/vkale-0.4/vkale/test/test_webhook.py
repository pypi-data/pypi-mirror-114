import unittest

from .test_data import *


class TestWebhooks(unittest.TestCase):
    def setUp(self):
        self.bot = get_bot()

    def test_webhooks(self):
        server_name = 'main'
        server = self.bot.groups.get_callback_server_by_name(group_id=TEST_GROUP_ID_POS, server_name=server_name)
        # delete
        if server:
            response = self.bot.groups.delete_callback_server_by_name(group_id=TEST_GROUP_ID_POS,
                                                                      server_name=server_name)
            self.assertEqual(response, 1, msg=response)

        server = self.bot.groups.get_callback_server_by_name(group_id=TEST_GROUP_ID_POS, server_name=server_name)
        self.assertIsNone(server, msg=server)

        # add
        server_id = self.bot.groups.add_callback_server(group_id=TEST_GROUP_ID_POS,
                                                        url=TEST_WEBHOOK_URL,
                                                        title=server_name)
        servers = self.bot.groups.get_callback_servers(group_id=TEST_GROUP_ID_POS, servers_id=[server_id])
        self.assertEqual(len(server), 1, server)
        server = servers[0]
        response = self.bot.groups.set_callback_settings(group_id=TEST_GROUP_ID_POS,
                                                         server_id=server.id,
                                                         message_new=1)
        self.assertEqual(response, 1, msg=response)

        # if not server.is_empty():
        #     response = self.bot.groups('editCallbackServer',
        #                                group_id=TEST_GROUP_ID_POS,
        #                                server_id=server_id,
        #                                url=TEST_WEBHOOK_URL,
        #                                title=server_name)
        # self.assertEqual(response, 1, msg=response)

        # get
        server = self.bot.groups.get_callback_servers(TEST_GROUP_ID_POS)
        self.assertNotEqual(server._data, [], msg=server._data)
        self.assertEqual(server._data[0].title, 'main', msg=server._data)
        self.assertEqual(server._data[0].url, TEST_WEBHOOK_URL, msg=server._data)


def test_callback(vk: VKaleAPI):
    servers = vk.groups.get_callback_servers(group_id=TEST_GROUP_ID_POS)
    for server in servers:
        settings = vk.groups.get_callback_settings(group_id=TEST_GROUP_ID_POS, server_id=server.id)
        print(settings.message_new)


if __name__ == '__main__':
    unittest.main()
