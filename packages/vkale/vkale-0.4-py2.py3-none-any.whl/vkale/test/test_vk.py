import random
import unittest

from .test_data import *


class TestBasic(unittest.TestCase):
    def setUp(self):
        self.vk = get_api()
        self.vk_bot = get_bot()

    # def test_user_name(self):
    def test_wall(self):
        text = f'test_text {random.randint(100, 100000)}'
        self.vk.wall.post(message=text, owner_id=TEST_GROUP_ID_NEG, from_group=1)
        self.vk.wall.post(message=text, owner_id=TEST_GROUP_ID_NEG, from_group=0)

        result = self.vk.wall.get(owner_id=TEST_GROUP_ID_NEG, count=10)
        self.assertEqual(len(result), 10, result)
        self.assertEqual(result[0].text, text, result)
        self.assertEqual(result[0].from_id, TEST_USER_ID, result)
        self.assertEqual(result[1].text, text, result)
        self.assertEqual(result[1].from_id, TEST_GROUP_ID_NEG, result)

    def test_get_friends(self):
        result = self.vk.friends.get(user_id=TEST_USER_ID, count=10)
        self.assertEqual(len(result.items), 10, result.items)

    def test_message(self):
        response = self.vk_bot.messages.send(message='test_msg', user_id=TEST_USER_ID, random_id=0)
        self.assertTrue(isinstance(response.response, int), response)


# def test_post_wall_rate_limit(vk: VKaleAPI):
#     for i in range(2):
#         for post_int in range(3):
#             test_post_wall(vk, text=f'test_post_{i}_{post_int}')


def test_message_send_rate_limit(vk: VKaleAPI):
    for i in range(4):
        for post_int in range(5):
            vk.method('messages.send', message=f'test_msg_{i}_{post_int}', user_id=TEST_USER_ID, random_id=0)


if __name__ == '__main__':
    unittest.main()

    # test_callback(vk_bot)
    # test_get_wall(vk)
    # test_get_friends(vk)
    # test_post_wall(vk, 'test_post_wall')

    # test_message(vk_bot)
    # test_message_send_rate_limit(vk_bot)
