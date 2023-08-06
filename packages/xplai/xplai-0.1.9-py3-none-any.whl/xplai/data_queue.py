#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

from multiprocessing import Process, Queue

from xplai.api import data_api_client
from xplai.api.data_api_client import DataPoint

DATA_POINT_QUEUE = Queue()


def queue_data_point(data_point: DataPoint):
    DATA_POINT_QUEUE.put(data_point)


def __sending_loop(queue: Queue):
    while True:
        try:
            data_point: DataPoint = queue.get()
            data_api_client.upload(data_point=data_point)
        except Exception:
            continue


data_sending_process = Process(target=__sending_loop, args=(DATA_POINT_QUEUE,))
data_sending_process.daemon = True
data_sending_process.start()
