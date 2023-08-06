#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

import csv
import uuid

from os.path import exists

from pydantic import BaseModel
from typing import List, Optional, Dict

from xplai.api.data_api_client import DataItem, DataPoint

from xplai.api import task_api_client, data_api_client
from xplai.api.task_api_client import TaskSetupFailedException, TaskSetupFailedInvalidInputException, TaskNotFoundException

from xplai.cli import concept
from xplai.cli.concept import Concept

from xplai import config
from xplai.cli import utils


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


OFFSET = '  '


def create_from_csv(name: str,
                    modality: str,
                    path_to_csv: str):
    task_draft = TaskDefinition(name=name,
                                modality=modality,
                                model_size='onesize')

    concept_definitions, errors = __read_csv(path_to_csv)
    if len(concept_definitions) > 0:
        task_draft.concept_definitions = concept_definitions

    if len(errors) > 0:
        errors_string = '\n'.join(errors)
        return errors_string

    __save_draft(task_draft)

    user_defined_concept_names = concept_definitions.keys()

    for idx, name in enumerate(user_defined_concept_names):
        print(f'\n{OFFSET}Which of the following best describes\t"{name}"?\n')

        search_results_text, concepts = concept.search(lemma=name, include_not_found_option=True)
        print(search_results_text)

        choice = input(f"{OFFSET}Please enter your numeric choice: ")
        selected_option = choice
        while not selected_option.isdigit():
            print('\nYou have entered an invalid option')
            option = input('Do you wish to continue? Enter your numeric choice: [1]Yes  [2]No')
            if int(option) == 1:
                print(f'\n{OFFSET}Which of the following best describes\t"{name}"?\n')
                search_results_text, concepts = concept.search(lemma=name, include_not_found_option=True)
                print(search_results_text)
                choice = input(f"{OFFSET}Please enter your numeric choice: ")
                selected_option = choice
            else:
                exit(0)
        selected_concept: Concept = concepts[int(selected_option)]
        print(f'{OFFSET}selected: [{int(selected_option)}] {selected_concept.name}')

        if selected_concept.concept_id is not None:
            concept_definitions[name].concept_id = selected_concept.concept_id
        elif selected_concept.wn_id is not None:
            concept_definitions[name].wn_id = selected_concept.wn_id
        concept_definitions[name].concept = selected_concept

        __save_draft(task_draft)

    return f'{OFFSET}Draft created. \n' \
           f'{__make_task_description_from_task_definition(task_draft)}\n' \
           f'{OFFSET}To commit draft and rollout active learning pipeline type:\n\n' \
           f'{OFFSET}{OFFSET}xpl task commit \n'


def create(name: str,
           modality: str):
    task_draft = TaskDefinition(name=name,
                                modality=modality,
                                model_size='m')

    __save_draft(task_draft)


def commit_draft():
    task_definition_draft = __load_draft()
    steps_count = '3'
    if task_definition_draft is None:
        return f'There are no active task drafts. Start creating new tasks by typing:\n\n' \
               f'xpl task create\n'
    try:
        print(f'\n{OFFSET}[Step 1 of {steps_count}] Initialize active learning pipeline.')
        fresh_task = task_api_client.setup_task_from_definition(task_definition=task_definition_draft)
        print(f'{OFFSET}[Step 1 of {steps_count}] Initialize active learning pipeline. Result: SUCCESS.')

        print(f'{OFFSET}')
        data_points = []
        print(f'{OFFSET}[Step 2 of {steps_count}] Prepare examples for upload.')
        for key, concept_definition in task_definition_draft.concept_definitions.items():
            for example in concept_definition.examples:
                display_name = key
                concept_id = None

                # TODO: Refactor Task object: make .concepts collection a dictionary of key=concept_id
                for c in fresh_task.concepts:
                    if c.display_name == display_name:
                        concept_id = c.concept_id

                if concept_id is None:
                    raise Exception(f'Could not resolve concept example '
                                    f'user_provided_concept_name={concept_definition.user_provided_concept_name} '
                                    f'example path_to_file "{example.path_to_file}"')

                with open(example.path_to_file, 'rb') as file:
                    file_bytes = file.read()
                    file_extension = example.path_to_file.split('.')[-1]
                    data_point = DataPoint(
                        task_id=fresh_task.task_id,
                        data_point_id=uuid.uuid4().hex,
                        binaries={f'input.{file_extension}': file_bytes},
                        file_uris=[],
                        collected_by_device_fingerprint_id=str(uuid.getnode()),
                        data_items=[
                            DataItem(
                                concept_id=concept_id,
                                instance_id=uuid.uuid4().hex,
                                predictor_type='user',
                                predictor_id='user',
                                input_set='train',
                                log_informativeness=0.0,
                                logit_confidence=1.0,
                                location=example.location.dict(exclude_none=True) if example.location is not None else None
                            )
                        ]
                    )
                    data_points.append(data_point)
                    # data_api_client.upload(data_point, task_api_key=fresh_task.client_api_key)
        print(f'{OFFSET}[Step 2 of {steps_count}] Prepare examples for upload. Result: SUCCESS\n')
        data_point_batches = __make_batches(data_points, n=50)
        uploaded_count = 0
        print(f'{OFFSET}[Step 3 of {steps_count}] Uploading examples data...')
        for batch in data_point_batches:
            data_api_client.upload_batch(data_points=batch,
                                         task_api_key=fresh_task.client_api_key)
            uploaded_count += len(batch)
            print(f'{OFFSET}[Step 3 of {steps_count}] Uploading examples data: Uploaded {uploaded_count} examples of {len(data_points)}')
        print(f'{OFFSET}[Step 3 of {steps_count}] Uploading examples data: Result: SUCCESS')

        summary_text = f'\n{OFFSET}Task committed. Active learning pipeline initialized.' \
                       f'\n{OFFSET}Summary:\n'
        summary_text += __make_task_description(fresh_task.dict())
        summary_text += f'\n{OFFSET}Model training started and will take up to 10 min to complete.'

        __discard_draft()

        return summary_text

    except TaskSetupFailedInvalidInputException as e_invalid_input:
        error_text = '\nTask setup failed:\n'
        if e_invalid_input.errors is not None:
            error_text += utils.print_table(e_invalid_input.errors, ['errors'])
        else:
            error_text += e_invalid_input.args[0]
        return error_text

    except TaskSetupFailedException as e_generic:
        return f'\nTask setup failed with error\n' \
               f'{e_generic.args[0]}'


def list_tasks():
    tasks = task_api_client.list_tasks()
    for task in tasks:
        if 'model' in task and task['model']:
            task['model_version'] = str(task['model']['version'])
        else:
            task['model_version'] = '[no model]'

    return utils.print_table(tasks, ['name', 'model_size', 'modality', 'task_id', 'created_on', 'model_version'])


def get(task_id: str):
    try:
        task = task_api_client.get_task(task_id)
        return task
    except TaskNotFoundException:
        return f'Task "{task_id}" not found.'
    except Exception:
        return f'Task "{task_id}" not found.'


def describe(task_id: str):
    task_id = input("Provide task name or task_id:") if task_id is None else task_id
    try:
        task = task_api_client.get_task(task_id)
        return __make_task_description(task)
    except TaskNotFoundException as e:
        return e.args[0]


def __make_task_description(task: Dict):
    model_version = task['model']['version'] if 'model' in task and task['model'] else '[no model]'

    description = f'\n' \
                  f'{OFFSET}task_id: {task["task_id"]}\n' \
                  f'{OFFSET}client_api_key: {task["client_api_key"]}\n' \
                  f'{OFFSET}name: {task["name"]}\n' \
                  f'{OFFSET}modality: {task["modality"]}\n' \
                  f'{OFFSET}model_size: {task["model_size"]}\n' \
                  f'{OFFSET}model_version: {model_version}\n' \
                  f'{OFFSET}created_on: {task["created_on"]}\n' \
                  f'{OFFSET}concepts:\n'

    concepts = utils.print_table(task['concepts'], ['concept_id', 'display_name'])
    description += concepts
    return description


def __make_task_description_from_task_definition(task_definition: TaskDefinition):
    concept_definitions = []
    for key, concept_definition in task_definition.concept_definitions.items():
        concept_definition_dict = concept_definition.dict()
        concept_definition_dict['display_name'] = concept_definition_dict['user_provided_concept_name']
        if concept_definition.concept is not None \
                and concept_definition.concept.definition:
            concept_definition_dict['definition'] = concept_definition.concept.definition
        else:
            concept_definition_dict['definition'] = concept_definition.user_provided_concept_definition
        concept_definitions.append(concept_definition_dict)

    description = f'\n' \
                  f'{OFFSET}name: {task_definition.name}\n' \
                  f'{OFFSET}modality: {task_definition.modality}\n' \
                  f'{OFFSET}model_size: {task_definition.model_size}\n' \
                  f'{OFFSET}concepts: \n' \
                  f'{utils.print_table(concept_definitions, ["concept_id", "display_name", "definition"])}'

    return description


def __read_csv(path_to_csv
               ) -> (Dict[str, ConceptDefinition], List[str]):
    with open(path_to_csv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        has_header = False
        first_row = next(iter(csv_reader))
        columns = {}
        if first_row[0].startswith('\ufeff'):
            first_row[0] = first_row[0].replace('\ufeff', '')
        if 'local_file_name' in first_row:
            has_header = True
            for i, name in enumerate(first_row):
                columns[name] = i
        if not has_header:
            columns = {
                'local_file_name': 0,
                'concept_name': 1,
                'center_x': 2,
                'center_y': 3,
                'half_width': 4,
                'half_height': 5,
                'center_t': 6,
                'half_period': 7
            }
        concept_drafts = {}

        all_errors = []
        for row_number, row in enumerate(csv_reader):
            user_provided_concept_name, example, errors = __parse_row(row=row,
                                                                      columns=columns,
                                                                      row_number=row_number)
            if len(errors) > 0:
                all_errors.extend(errors)
                continue

            if user_provided_concept_name in concept_drafts:
                draft = concept_drafts[user_provided_concept_name]
                draft.examples.append(example)
            else:
                draft = ConceptDefinition(
                    user_provided_concept_name=row[columns['concept_name']],
                    examples=[example]
                )
                concept_drafts[user_provided_concept_name] = draft

        return concept_drafts, all_errors


def __parse_row(row: List,
                columns: Dict[str, int],
                row_number: int
                ) -> (str, ConceptExample, List[str]):
    errors = []
    path_to_file = row[columns['local_file_name']]
    if not __file_exists(path_to_file):
        errors.append(f'row={row_number}, file not found path={path_to_file}')

    user_provided_concept_name: str = row[columns['concept_name']]
    example = None
    try:
        example = ConceptExample(
            path_to_file=row[columns['local_file_name']]
        )

        if 'center_x' in columns and row[columns['center_x']] and \
                'half_width' in columns and row[columns['half_width']]:
            location = Location(
                center_x=row[columns['center_x']],
                half_width=row[columns['half_width']]
            )
            example.location = location
            if 'center_y' in columns and row[columns['center_y']] and \
                    'half_height' in columns and row[columns['half_height']]:
                location.center_y = row[columns['center_y']]
                location.half_height = row[columns['half_height']]
                if 'center_t' in columns and row[columns['center_t']] and \
                        'half_period' in columns and row[columns['half_period']]:
                    location.center_t = row[columns['center_t']]
                    location.half_period = row[columns['half_period']]
    except Exception as e:
        error = ''
        for arg in e.args:
            error += f'\t{arg}'
        errors.append(f'row={row_number}, {error}')
    return user_provided_concept_name, example, errors


def __file_exists(path):
    return exists(path) and exists(path)


def __save_draft(task_definition: TaskDefinition):
    config['current_task_definition_draft'] = task_definition.dict()
    config.save()


def __load_draft():
    if 'current_task_definition_draft' in config and \
            config['current_task_definition_draft'] is not None:
        return TaskDefinition(**config['current_task_definition_draft'])
    return None


def __discard_draft():
    if 'current_task_definition_draft' in config and \
            config['current_task_definition_draft'] is not None:
        del config['current_task_definition_draft']
        config.save()


def __make_batches(items: List,
                   n=50
                   ) -> List[List]:
    return [items[i * n:(i + 1) * n] for i in range((len(items) + n - 1) // n)]
