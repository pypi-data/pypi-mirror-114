import requests

from vkale import enums


# region scope
def get_permissions_mask(permissions: list[enums.UserPermissions]) -> int:
    return sum(permissions)


def get_permissions_mask_from_str(permissions: list[str]) -> int:
    permissions = [enums.UserPermissions[p] for p in permissions]
    return get_permissions_mask(permissions)


# endregion

def get_auth_code(client_id, redirect_uri='https://oauth.vk.com/blank.html', display='page', scope: int = 0, response_type='token',
                  state='smyek'):
    values = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'display': display,
        'scope': scope,
        'response_type': response_type,
        'state': state
    }
    request = requests.request('post', 'https://oauth.vk.com/authorize', data=values)
    url = request.url + '?' + request.request.body
    return url


def code_auth(self, code, redirect_url):
    """ Получение access_token из code """
    values = {
        'client_id': self.app_id,
        'client_secret': self.client_secret,
        'v': self.api_version,
        'redirect_uri': redirect_url,
        'code': code,
    }

    response = requests.post('https://oauth.vk.com/access_token', values).json()

    if 'error' in response:
        raise Exception(response['error_description'])
    else:
        self.token = response
    return response


if __name__ == '__main__':
    permissions_example = [enums.UserPermissions.wall, enums.UserPermissions.offline]
    print("from enums:", get_permissions_mask(permissions_example))

    permissions_example = ['wall', 'offline', 'messages']
    print("from str:", get_permissions_mask_from_str(permissions_example))

    scope = get_permissions_mask_from_str(permissions_example)

    auth_res = get_auth_code('7847621', scope=scope)
    print(auth_res)
