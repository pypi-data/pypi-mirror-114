import unittest

from .test_data import *


class TestUsers(unittest.TestCase):
    def test_user_name(self):
        vk = get_bot()
        users = vk.users.get(user_ids=1)
        self.assertEqual(users[0].first_name, 'Павел')
        self.assertEqual(users[0].last_name, 'Дуров')

    def test_wall(self):
        vk = get_api()
        wall = vk.wall.get(owner_id=1, count=1)
        self.assertTrue('Telegram' in wall[0].text)


if __name__ == '__main__':
    unittest.main()
