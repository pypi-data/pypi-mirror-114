#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

import io
import os
import uuid

from typing import List

import requests
import torch
import torchvision

from PIL import Image

from torchvision.utils import save_image, make_grid

from matplotlib import pyplot

from xplai import config
from xplai import utils

from xplai.api.data_api_client import DataItem, DataPoint
from xplai.api import data_api_client, task_api_client
from xplai.api.task_api_client import PublicTaskResource, TaskConceptResource


class Task:
    def __init__(self,
                 task_id: str,
                 task_api_key: str = None):
        self.__task_id = task_id
        self.__task_api_key = task_api_key
        self.__task_data = self.reload_task(task_id=self.__task_id,
                                            task_api_key=self.__task_api_key)
        self.__model = {}
        for component_name, component in self.__task_data.model.components.items():
            component = self.__load_model_component_from_disk(component_name=component_name)
            self.__model[component_name] = component
            self.__model[component_name].eval()
        self.concepts = {}

        for concept in self.__task_data.concepts:
            self.concepts[concept.concept_id] = concept

    def reload_task(self,
                    task_id: str,
                    task_api_key: str = None):
        server_task_data = None
        local_task_data = None

        try:
            server_task_data: PublicTaskResource = task_api_client.get_public_task(task_id=task_id,
                                                                                   task_api_key=task_api_key)
            if server_task_data.model is None:
                raise Exception(f'Model for task {task_id} does not exist.')
        except:
            """ Tolerate failure to call and give a chance to load from the disk.
                Most of the time model will be already downloaded."""
            pass

        if 'tasks' in config and task_id in config['tasks']:
            local_task_data = PublicTaskResource(**config['tasks'][self.__task_id])

        if not server_task_data and not local_task_data:
            raise TaskNotFoundException

        if server_task_data and local_task_data:
            if server_task_data.model.version != local_task_data.model.version:
                for key_name, model_component in server_task_data.model.components.items():
                    self.__download_model_component(url_for_download=model_component.url_for_download,
                                                    component_name=key_name)
                config['tasks'][server_task_data.task_id] = server_task_data.dict()
                local_task_data = server_task_data
                config.save()

        if server_task_data and not local_task_data:
            for key_name, model_component in server_task_data.model.components.items():
                self.__download_model_component(url_for_download=model_component.url_for_download,
                                                component_name=key_name)
            local_task_data = server_task_data
            if 'tasks' in config:
                config['tasks'][server_task_data.task_id] = local_task_data.dict()
            else:
                config['tasks'] = {}
                config['tasks'][server_task_data.task_id] = local_task_data.dict()
            config.save()

        # """we should have model file at this point"""
        # if not os.path.exists(self.__get_model_component_file_name()):
        #     raise Exception()

        return local_task_data

    def queue_data_point_for_upload(self,
                                    data_point: DataPoint):
        """Sends datapoints for upload to the data process over the queue and releases control.
            Currently uploads synchronously in order not to obscure data and logic related errors at the early stage of development.
        """

        data_api_client.upload_batch(data_points=[data_point],
                                     task_api_key=self.__task_api_key)

    def __download_model_component(self,
                                   url_for_download: str,
                                   component_name: str):
        """download model from the cloud using temporary authenticated url"""
        response = requests.get(url_for_download)

        if response.status_code == 200:
            with open(self.__get_model_component_file_name(component_name=component_name), 'wb') as file:
                file.write(response.content)
                return

        raise SystemError('Downloading model failed')

    def __get_model_component_file_name(self,
                                        component_name: str):
        return os.path.join(config.get_home_dir(), f'{self.__task_id}__{component_name}')

    def __load_model_component_from_disk(self,
                                         component_name: str):
        """load torch model from disk"""
        model_file_name = self.__get_model_component_file_name(component_name=component_name)
        model = torch.jit.load(model_file_name)

        return model

    def run(self, source: str
            ) -> List[TaskConceptResource]:
        image = utils.load_image_from_disk(source)
        image = torchvision.transforms.Resize((256, 256))(image)
        image = image.unsqueeze(0)

        image_rep = self.__model['image_rep.pts'](image)
        result_tensor = self.__model[self.__task_data.name + '.pts'](image_rep)

        max_result, _ = result_tensor.max(-1)
        max_result, _ = max_result.max(-1)

        final_result = torch.argmax(max_result).item() - 1
        concept_id = self.__task_data.model.output[str(final_result)]

        grid = make_grid(image[0])
        # Add 0.5 after unnormalizing to [0, 255] to round to nearest integer
        ndarr = grid.mul(255).add_(0.5).clamp_(0, 255).permute(1, 2, 0).to('cpu', torch.uint8).numpy()
        im = Image.fromarray(ndarr)
        bytes_io = io.BytesIO()
        im.save(bytes_io, format='png')
        image_bytes = bytes_io.getvalue()

        file_extension = 'png'
        data_point = DataPoint(
            task_id=self.__task_id,
            data_point_id=uuid.uuid4().hex,
            binaries={f'input.{file_extension}': image_bytes},
            file_uris=[],
            collected_by_device_fingerprint_id=str(uuid.getnode()),
            data_items=[
                DataItem(
                    concept_id=concept_id,
                    instance_id=uuid.uuid4().hex,
                    predictor_type='model',
                    predictor_id=self.__task_data.model.model_id,
                    input_set='train',
                    log_informativeness=0.0,
                    logit_confidence=1.0,
                    location={'center_x': 0.5,
                              'center_y': 0.5,
                              'half_width': 0.5,
                              'half_height': 0.5}
                )
            ]
        )

        self.queue_data_point_for_upload(data_point=data_point)

        render = False
        if render:
            self.__render(tensor=final_result[0][0],
                          label=self.concepts[concept_id].display_name)

        return [self.concepts[concept_id]]

    def __render(self,
                 tensor: torch.Tensor,
                 label: str):
        to_pillow = torchvision.transforms.ToPILImage()
        pyplot.imshow(to_pillow(tensor))
        pyplot.title(f'{self.concepts[label]}', fontsize=8)


class TaskNotFoundException(Exception):
    pass
