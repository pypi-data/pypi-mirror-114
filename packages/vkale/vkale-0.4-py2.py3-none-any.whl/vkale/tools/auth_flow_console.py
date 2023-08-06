from vkale.tools.auth_flow import get_permissions_mask_from_str, get_auth_code


if __name__ == '__main__':
    # e.g. 'wall offline messages'
    app_id = input('app_id: ').strip()
    permissions = input('permissions (e.g. wall offline messages): ').strip().split()
    scope = get_permissions_mask_from_str(permissions)

    auth_res = get_auth_code(app_id, scope=scope)
    print(auth_res)