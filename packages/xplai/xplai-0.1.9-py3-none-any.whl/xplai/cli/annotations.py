#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

from xplai import config
from xplai.api import annotation_api_client

from xplai.cli.utils import print_table


def list_annotation_jobs(task_id: str):
    annotation_jobs = annotation_api_client.list_annotation_jobs(task_id=task_id)

    for annotation_job in annotation_jobs:
        annotation_job['concept_name'] = annotation_job['concept']['name']
        annotation_job['number of frames'] = str(len(annotation_job['instance_frames']))
        annotation_job['job_url'] = f'{config.ANNOTATION_API_URI}/job/{annotation_job["annotation_job_id"]}/annotate'
    return print_table(annotation_jobs, ['job_url', 'concept_name', 'number of frames'])
