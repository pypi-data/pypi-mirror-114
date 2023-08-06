#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

from xplai import config
from xplai.api import auth_api_client

OFFSET = '  '


def login(username: str,
          secret: str
          ) -> str:
    login_result = auth_api_client.login(username=username,
                                         secret=secret)

    if login_result.successful is True:
        config['api_key'] = login_result.api_key
        config['username'] = login_result.username
        config.save()

        return f'\n{OFFSET}Logged in successfully as {username}\n'

    return f'\n{OFFSET}Login failed\n'


def logout() -> str:
    if 'api_key' in config:
        del config['api_key']
    if 'username' in config:
        del config['username']
    config.save()

    return f'\n{OFFSET}Logged out\n'


def get_cached_api_key() -> (str, str):
    return config['api_key'], config['username']


def get_api_headers():
    api_key, username = get_cached_api_key()
    return {'api_key': api_key, 'username': username}
