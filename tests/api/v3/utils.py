

# @TODO complete fully with correct info

# for admin user
def get_auth_header_admin():
    return {'AUTH': 'admin:admin_api_key'}

# for standard user


def get_auth_header_user():
    return {'AUTH': 'demo:demo_api_key'}

# invalid auth credentials


def get_auth_header_invalid():
    return {'AUTH': 'not_a_user:invalid_api_key'}
