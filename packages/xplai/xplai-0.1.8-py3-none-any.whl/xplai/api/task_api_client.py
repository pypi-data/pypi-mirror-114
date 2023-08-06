#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

import json

import requests

from pydantic import BaseModel
from typing import List, Optional, Dict

from xplai.api.concept_api_client import Concept
from xplai import config


class Location(BaseModel):
    center_x: Optional[float]
    center_y: Optional[float]
    center_t: Optional[float]
    half_width: Optional[float]
    half_height: Optional[float]
    half_period: Optional[float]


class ConceptExample(BaseModel):
    path_to_file: str
    location: Optional[Location]


class ConceptDefinition(BaseModel):
    user_provided_concept_name: str
    user_provided_concept_definition: Optional[str]
    wn_id: Optional[str]
    concept_id: Optional[str]

    concept: Optional[Concept]
    examples: Optional[List[ConceptExample]]


class TaskDefinition(BaseModel):
    name: str
    modality: str
    model_size: str
    concept_definitions: Optional[Dict[str, ConceptDefinition]]


class TaskConceptResource(BaseModel):
    display_name: str
    concept_id: str


class ModelComponentResource(BaseModel):
    url_for_download: str
    name: str


class ModelResource(BaseModel):
    model_id: Optional[str]
    components: Dict[str, ModelComponentResource]
    output: Optional[Dict[str, str]]
    version: int


class TaskResource(BaseModel):
    task_id: str
    name: str
    client_api_key: str
    modality: str
    concepts: List[TaskConceptResource]
    model_size: str
    created_on: Optional[str]
    model: Optional[ModelResource]


class PublicTaskResource(BaseModel):
    task_id: str
    name: str
    concepts: List[TaskConceptResource]
    model: Optional[ModelResource]


class TaskNotFoundException(Exception):
    pass


class TaskSetupFailedException(Exception):
    pass


class TaskSetupFailedInvalidInputException(Exception):
    def __init__(self, message=None, errors: List = None):
        super().__init__(message)
        self.errors = errors


def setup_task_from_definition(task_definition: TaskDefinition
                               ) -> TaskResource:
    task_definition_payload = {
        'name': task_definition.name,
        'modality': task_definition.modality,
        'model_size': task_definition.model_size,
        'concept_definitions': []
    }

    for key, concept_definition in task_definition.concept_definitions.items():
        task_definition_payload['concept_definitions'].append(
            {
                'concept_id': concept_definition.concept_id,
                'wn_id': concept_definition.wn_id,
                'user_provided_concept_name': concept_definition.user_provided_concept_name,
                'user_provided_concept_definition': concept_definition.user_provided_concept_definition
            }
        )

    response = requests.post(url=f'{config.USER_API_URI}/task',
                             headers=config.get_api_headers(),
                             json=task_definition_payload)

    if response.status_code == 422:
        try:
            json_errors = json.loads(response.text)
            if 'errors' in json_errors:
                raise TaskSetupFailedInvalidInputException(errors=json_errors)
            raise TaskSetupFailedInvalidInputException(message=response.text)
        except Exception as e:
            raise TaskSetupFailedInvalidInputException(message=response.text)

    if response.status_code != 200:
        raise TaskSetupFailedException(response.text)

    return TaskResource(**json.loads(response.text))


def list_tasks():
    response = requests.get(url=f'{config.USER_API_URI}/tasks',
                            headers=config.get_api_headers())
    if response.status_code != 200:
        raise Exception(f'Http error {response.status_code}.')

    tasks = json.loads(response.text)
    return tasks


def get_task(task_id: str):
    response = requests.get(url=f'{config.USER_API_URI}/task/{task_id}',
                            headers=config.get_api_headers())
    if response.status_code == 404:
        raise TaskNotFoundException(f'Task "{task_id}" not found.')

    elif response.status_code != 200:
        raise Exception(f'Http error {response.status_code}.')

    return json.loads(response.text)


def get_public_task(task_id: str,
                    task_api_key: str
                    ) -> PublicTaskResource:
    response = requests.get(url=f'{config.USER_API_URI}/task/{task_id}',
                            headers={'task_api_key': task_api_key})
    if response.status_code == 404:
        raise TaskNotFoundException(f'Task "{task_id}" not found.')

    elif response.status_code != 200:
        raise Exception(f'Http error {response.status_code}.')

    return PublicTaskResource(**json.loads(response.text))
