#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

import json
import requests

from xplai import config


def get_supported_modalities():
    response = requests.get(url=f'{config.USER_API_URI}/modalities')
    modalities = json.loads(response.text)
    return modalities
