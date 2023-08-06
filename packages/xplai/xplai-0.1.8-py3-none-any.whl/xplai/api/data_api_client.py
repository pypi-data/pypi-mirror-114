#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

import asyncio
import json

import requests

from pydantic import BaseModel
from typing import Optional, Dict, List

import aiohttp
import aiohttp.client_exceptions

from xplai import config


class DataItem(BaseModel):
    concept_id: str
    instance_id: str
    predictor_type: str
    predictor_id: str
    input_set: str
    log_informativeness: float
    logit_confidence: float
    location: Optional[Dict[str, Optional[float]]]


class DataPoint(BaseModel):
    task_id: str
    data_point_id: str
    binaries: Optional[Dict[str, bytes]]
    file_uris: List[str]
    data_items: List[DataItem]
    previous_data_point_id: Optional[str]
    next_data_point_id: Optional[str]
    collected_by_device_fingerprint_id: Optional[str]


class UploadDataPointException(Exception):
    pass


def upload(data_point: DataPoint,
           task_api_key: str):
    file_names = list(data_point.binaries.keys())
    file_names.append('data_point.json')

    response = requests.post(url=f'{config.DATA_API_URI}/upload/{data_point.task_id}/{data_point.data_point_id}',
                             json=file_names,
                             headers={'task_api_key': task_api_key})

    if response.status_code != 200:
        raise UploadDataPointException(f'http_status_code={response.status_code}', 'Failed to get URLs for upload.')

    upload_urls = json.loads(response.text)
    for key, bytes_value in data_point.binaries.items():
        """Upload binaries using generated upload urls """
        response = requests.post(url=upload_urls[key]['url_for_upload'],
                                 data=bytes_value)
        if response.status_code != 200:
            raise UploadDataPointException(f'http_status_code={response.status_code}', 'Failed to get URLs for upload.')

        data_point.file_uris.append(upload_urls[key]['url'])

    """Upload DataPoint's data file."""
    data_point.binaries = None
    requests.post(url=upload_urls['data_point.json']['url_for_upload'],
                  data=json.dumps(data_point.dict(), indent=4))


async def upload_async(data_point: DataPoint,
                       task_api_key: str,
                       session: aiohttp.ClientSession
                       ) -> DataPoint:
    file_names = list(data_point.binaries.keys())
    file_names.append('data_point.json')
    post_result, received_bytes = await __post_bytes(
        post_url=f'{config.DATA_API_URI}/upload/{data_point.task_id}/{data_point.data_point_id}',
        headers={'task_api_key': task_api_key, 'content-type': 'application/json'},
        bytes_to_post=json.dumps(file_names).encode('utf-8'),
        session=session)

    if post_result != str(200):
        raise UploadDataPointException(f'http_status_code={post_result}', 'Failed to get URLs for upload.')

    upload_urls = json.loads(received_bytes.decode('UTF-8'))
    for key, bytes_value in data_point.binaries.items():
        """Upload binaries using generated upload urls """
        post_result, _ = await __post_bytes(post_url=upload_urls[key]['url_for_upload'],
                                            bytes_to_post=bytes_value,
                                            session=session)
        if post_result != str(200):
            raise UploadDataPointException(f'status={post_result}', 'Failed to upload binaries.')
        data_point.file_uris.append(upload_urls[key]['url'])

    """Upload DataPoint's data file."""
    data_point.binaries = None
    post_result, _ = await __post_bytes(post_url=upload_urls['data_point.json']['url_for_upload'],
                                        bytes_to_post=json.dumps(data_point.dict(), indent=4).encode('utf-8'),
                                        session=session)
    if post_result != str(200):
        raise UploadDataPointException(f'status={post_result}', 'Failed to upload data_point.json.')

    return data_point


async def upload_batch_async(data_points: List[DataPoint],
                             task_api_key: str):
    async with aiohttp.ClientSession() as session:
        coroutines = []
        for data_point in data_points:
            coroutines.append(upload_async(data_point=data_point,
                                           task_api_key=task_api_key,
                                           session=session))
        data_points: List[DataPoint] = await asyncio.gather(*coroutines)
        data_points_list_of_dict = [p.dict() for p in data_points]
        post_result, _ = await __post_bytes(post_url=f'{config.DATA_API_URI}/datapoints',
                                            bytes_to_post=json.dumps(data_points_list_of_dict, indent=4).encode('utf-8'),
                                            session=session,
                                            headers={'task_api_key': task_api_key, 'content-type': 'application/json'})
        if post_result == str(401):
            raise UploadDataPointException(f'http_status_code={post_result}', 'Failed to upload DataPoints.')

        if post_result != str(200):
            raise UploadDataPointException(f'http_status_code={post_result}', 'Failed to upload DataPoints.')


def upload_batch(data_points: List[DataPoint],
                 task_api_key: str):
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(upload_batch_async(data_points, task_api_key))
    return results


async def __post_bytes(bytes_to_post: bytes,
                       post_url: str,
                       session: aiohttp.ClientSession,
                       headers: dict = None,
                       retry_count: int = 0
                       ) -> (str,):
    try:
        response = await session.post(url=post_url,
                                      data=bytes_to_post,
                                      headers=headers)
        http_status = response.status
        if http_status == 200:
            return str(http_status), await response.read()
        if http_status == 500:
            retry_count += 1
            if retry_count < 4:
                print('500, retry')
                return await __post_bytes(bytes_to_post=bytes_to_post,
                                          post_url=post_url,
                                          session=session,
                                          headers=headers,
                                          retry_count=retry_count)
        return str(http_status), None
    except aiohttp.ClientConnectorError:
        retry_count += 1
        if retry_count < 4:
            print('ClientConnectorError, retry')
            return await __post_bytes(bytes_to_post=bytes_to_post,
                                      post_url=post_url,
                                      session=session,
                                      headers=headers,
                                      retry_count=retry_count)
        return str(900), None
    except asyncio.TimeoutError:
        retry_count += 1
        if retry_count < 4:
            print('TimeoutError, retry')
            return await __post_bytes(bytes_to_post=bytes_to_post,
                                      post_url=post_url,
                                      session=session,
                                      headers=headers,
                                      retry_count=retry_count)
        return str(901), None
    except aiohttp.ClientOSError as e:
        retry_count += 1
        if retry_count < 4:
            print('ClientOSError, retry')
            return await __post_bytes(bytes_to_post=bytes_to_post,
                                      post_url=post_url,
                                      session=session,
                                      headers=headers,
                                      retry_count=retry_count)
        return str(902), None
    except aiohttp.ServerDisconnectedError as e:
        retry_count += 1
        if retry_count < 4:
            print('ServerDisconnectedError, retry')
            return await __post_bytes(bytes_to_post=bytes_to_post,
                                      post_url=post_url,
                                      session=session,
                                      headers=headers,
                                      retry_count=retry_count)
        return str(903), None
