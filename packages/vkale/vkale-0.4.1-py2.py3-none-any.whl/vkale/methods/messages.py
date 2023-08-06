from vkale.method import *


class Messages(VKMethodGroup):
    _name = 'messages'

    def __init__(self, vk_api):
        super().__init__(vk_api)
        self.send = Send(self)


class Send(VKMethod):
    _name = 'send'

    # _result_handler = MessagesSendResult

    def __call__(self, message: str, user_id: int, random_id=0, **kwargs):
        return self.request(dict(message=message, user_id=user_id, random_id=random_id, **kwargs))
