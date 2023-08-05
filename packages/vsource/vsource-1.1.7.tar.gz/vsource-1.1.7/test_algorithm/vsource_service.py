import os
import copy
import time
import json
import uuid
import redis
import kafka
import shutil
import requests
import traceback
import numpy as np

from urllib.request import urlopen

import vsource_configs

import random_number

class Service:
    def __init__(self):
        self.redis_host = vsource_configs.app_redis_hostname
        self.redis_port = vsource_configs.app_redis_port
        self.INFO_KEY = vsource_configs.app_info_key
        self.RESPONSE_KEY = vsource_configs.app_response_key
        self.ERROR_KEY = vsource_configs.app_error_key
        self.group_id = vsource_configs.app_group_id
        self.storage_host = vsource_configs.app_storage_host
        self.algorithm_name = vsource_configs.app_algorithm_full_name

    def read_file(self, path):
        # /get_files/<namespace>/<user>/<timestamp>/<filename>
        file_url =  self.storage_host + '/get_files/' + path
        dir_path = os.path.dirname(os.path.join('tmp', path))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_bytes = urlopen(file_url).read()
        with open(os.path.join('tmp', path), 'wb') as f:
            f.write(file_bytes)
        return os.path.join('tmp', path)

    def write_file(self, path):
        filename = os.path.split(path)[-1]
        upload_url = self.storage_host + '/upload_files' + '/tmp/tmp'
        with open(path, 'rb') as f:
            files = {'file': (filename, f.read())}
        response =  requests.post(upload_url, files=files)
        return json.loads(response.content)['return_path']

    def function(self, info_dict):
        try:
            lower = info_dict['lower']
            lower = float(lower)
            upper = info_dict['upper']
            upper = float(upper)
            out = random_number.random_number(lower, upper)
            return out

        except Exception as e:
            traceback.print_exc()
            return -1


    def start(self):
        print('[Calculator Init]', self.algorithm_name, 'Service Starting...')
        r = redis.Redis(host=self.redis_host, port=self.redis_port)
        time.sleep(vsource_configs.sleep_interval)
        print('[Calculator Init] Init Successfully!')
        while True:
            try:
                consumer = kafka.KafkaConsumer(vsource_configs.app_kafka_topic,
                                               group_id=self.group_id
                                               ,bootstrap_servers=[vsource_configs.app_kafka_host])
                for msg in consumer:
                    info_str = msg.value
                    try:
                        if not info_str or info_str is None:
                            time.sleep(vsource_configs.call_interval)
                            continue

                        info_str = str(info_str, encoding="utf-8")
                        print(info_str)
                        info = json.loads(info_str)

                        result = self.function(info)

                        if result == -1:
                            err_msg = self.algorithm_name.lower() + "Service Error."
                            raise Exception(err_msg)

                        ans = copy.deepcopy(info)
                        ans['status'] = 'finished'
                        ans['result'] = result
                        ans_str = json.dumps(ans)
                        assert r.rpush(self.RESPONSE_KEY, ans_str)
                        if os.path.exists('tmp'):
                            shutil.rmtree('tmp')
                    except Exception as e:
                        traceback.print_exc()
                        assert r.rpush(self.ERROR_KEY, info_str)
                        continue
            except Exception as e:
                traceback.print_exc()
                time.sleep(vsource_configs.call_interval)
                continue


if __name__ == '__main__':
    service = Service()
    service.start()
