#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

import json

import requests

from pydantic import BaseModel
from typing import Optional

from xplai import config


def list_annotation_jobs(task_id: str):
    response = requests.get(url=f'{config.ANNOTATION_API_URI}/jobs/{task_id}',
                            headers=config.get_api_headers())
    if response.status_code != 200:
        raise Exception(f'Http error {response.status_code}.')

    jobs = json.loads(response.text)
    return jobs
