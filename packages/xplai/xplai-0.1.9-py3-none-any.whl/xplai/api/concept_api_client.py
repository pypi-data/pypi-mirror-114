#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

import json

import requests

from pydantic import BaseModel
from typing import Optional, List

from xplai import config


class Concept(BaseModel):
    concept_id: Optional[str]
    name: str
    definition: Optional[str]
    wn_id: Optional[str]
    pos: Optional[str]


class ConceptApiException(Exception):
    pass


def search(lemma: str,
           ) -> (List[Concept]):
    uri = f'{config.USER_API_URI}/concept?lemma={lemma}'

    response = requests.get(url=uri,
                            headers=config.get_api_headers())

    if response.status_code != 200:
        raise ConceptApiException(f'HTTP Error {response.status_code}')

    search_results = []
    found = json.loads(response.text)

    for idx, c in enumerate(found):
        concept = Concept(**c)
        search_results.append(concept)

    return search_results
