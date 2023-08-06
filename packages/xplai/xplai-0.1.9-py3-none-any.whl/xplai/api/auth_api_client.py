#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

import json

import requests

from pydantic import BaseModel
from typing import Optional

from xplai import config


class LoginResult(BaseModel):
    successful: bool
    api_key: Optional[str]
    username: Optional[str]


def login(username: str,
          secret: str
          ) -> LoginResult:
    credentials = {'username': username, 'secret': secret}

    response = requests.post(url=f'{config.USER_API_URI}/login',
                             json=credentials)

    if response.status_code == 200:
        key = json.loads(response.text)
        return LoginResult(successful=True,
                           api_key=key['api_key'],
                           username=username)

    return LoginResult(successful=False)
