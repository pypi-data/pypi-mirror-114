# coding: utf-8
import json
import os
import time
import inspect
import random
# import pymongo
import atexit
import subprocess

from multiprocessing import Process, Queue
from hashlib import md5
from functools import singledispatch
from datetime import datetime
from functools import partial

from ..Utils.Log import Logger
from .WeChatAssistant import WeChatAssistant

def get_md5_hash(obj):
    md5_obj = md5()
    md5_obj.update(obj.encode('utf8'))
    return md5_obj.hexdigest()

def retrieve_name(var):
        """
        Gets the name of var. Does it from the out most frame inner-wards.
        :param var: variable to get name from.
        :return: string
        """
        for fi in reversed(inspect.stack()):
            names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
            if len(names) > 0:
                return names[0]

def get_commit_id():
    return subprocess.getoutput("git log -1 | grep commit | awk '{print $2}'")


def check_dict(obj):
    for k, v in obj.items():
        if type(v) is dict:
            obj[k] = check_dict(v)
        else:
            if 'tolist' in dir(v):
                obj[k] = v.tolist()
    return obj

class ParameterWatcher(object):

    # @classmethod
    # def config_mongodb_server(cls, host:str, ip:int, username:str, password:str):
    #     cls.mongodb = dict()
    #     cls.mongodb['host'] = host
    #     cls.mongodb['port'] = port
    #     cls.mongodb['username'] = username
    #     cls.mongodb['password'] = password

    #     cls.myclient = pymongo.MongoClient(host=cls.mongodb['host'], port=cls.mongodb['host'], connect=False)
    #     # cls.myclient = pymongo.MongoClient("mongodb://47.103.90.218:8752/", connect=False)
    #     cls.db = cls.myclient.admin
    #     cls.db.authenticate(cls.mongodb['username'], cls.mongodb['password'])
        
    #     cls._mongodb_configed = True
        

    @classmethod
    def run_save(cls):
        if hasattr(cls, 'save_proc'):
            Logger.get_logger().warning("Already have one saving process...")
            return False
        Logger.get_logger().info("Starting saving process...")
        cls.save_proc = Process(target=cls.save_to_file)
        # save_proc.daemon = True 
        # Cannot set save process to daemon, otherwise save process will interupt once main thread exits.
        cls.save_proc.start()
        return True
    
    @classmethod
    def terminate_save_proc(cls):
        if cls.save_proc:
            Logger.get_logger().warning("Saving process will terminate in 5s...")
            time.sleep(5)
            remain_wait_round = 10
            while not cls.WATCHER_QUEUE.empty():
                Logger.get_logger().warning("Queue is not empty, waiting save_proc to finish remain queue tasks")
                time.sleep(2)
                if remain_wait_round == 0:
                    break
                remain_wait_round -= 1
            cls.save_proc.terminate()
            Logger.get_logger().info("Closing saving process...")
            return True
        else:
            Logger.get_logger().warning("No saving process can be terminated...")
            return False
    
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls, 'WATCHER_QUEUE'):
            pass
            # cls.WATCHER_QUEUE = Queue()
            # cls.run_save()
        return super().__new__(cls)

    def __init__(self, name, local_save=True, enable_wechat_notification=False):
        atexit.register(self.close_save)
        self.parameters = dict()
        self.model_parameters = dict()
        self.training_parameters = dict()
        self.miscellaneous_parameters = dict()
        self.data_parameters = dict()
        self.models = dict()
        self.results = dict()
        self.id = get_md5_hash(f'{name}-{time.time()}-{random.random()}')
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.start_time_stamp = time.time()
        self.name = name
        self.description = name
        self.save_dir = f'~/.nlutils/params/{self.name}' # Avoid sudo access requirement
        self.local_save = local_save
        self.enable_wechat_notification = enable_wechat_notification
        self.wechat_bot = None
        if self.enable_wechat_notification:
            self.wechat_bot = WeChatAssistant()

    def close_save(self):
        if not self.local_save:
            return
        if len(self.results) == 0:
            if 'fail' in self.save_dir:
                pass
            else:
                self.save_dir = f'{self.save_dir}/fail'
                Logger.get_logger().warning("No results saved, experiment could be interrupted during the training...")
        os.makedirs(self.save_dir, exist_ok=True)
        if 'fail' not in self.save_dir:
            os.makedirs(f'{self.save_dir}/{self.time[:10]}', exist_ok=True)
        whole_data = dict()
        basic_data = dict()
        basic_data['name'] = self.name
        basic_data['description'] = self.description
        basic_data['time'] = self.time
        basic_data['start_time_stamp'] = self.start_time_stamp
        basic_data['end_time_stamp'] = time.time()
        basic_data['time_consumed'] = basic_data['end_time_stamp'] - self.start_time_stamp
        basic_data['id'] = self.id
        basic_data['commit_id'] = get_commit_id()
        whole_data['parameters'] = self.parameters
        whole_data['model_parameters'] = self.model_parameters
        whole_data['training_parameters'] = self.training_parameters
        whole_data['data_parameters'] = self.data_parameters
        whole_data['miscellaneous_parameters'] = self.data_parameters
        whole_data['models'] = self.models
        whole_data['results'] = self.results
        hash_code = get_md5_hash(whole_data.__str__())
        basic_data['hash_code'] = hash_code
        whole_data['basic_parameters'] = basic_data
        whole_data = check_dict(whole_data)
        # TODO: Use template to make it better
        self.wechat_bot.send_to_filehelper(whole_data.__str__())
        if 'fail' in self.save_dir:
            with open(f"{self.save_dir}/{self.name}-{self.time}-{self.id}.json", "w") as f:
                json.dump(whole_data, f)
        else:
            with open(f"{self.save_dir}/{self.time[:10]}/{self.name}-{self.time}-{self.id}.json", "w") as f:
                json.dump(whole_data, f)
    
    def disable_local_save(self):
        self.local_save = False

    def enable_local_save(self):
        self.local_save = True

    def set_parameter_by_argparser(self, args):
        parameters = {f'{key}': val for key, val in args._get_kwargs()}
        self.set_parameters(parameters)
    
    def set_parameters(self, parameters):
        self.parameters = parameters
    
    def insert_update(self, container, key, value):
        container[key] = value if str(value) != 'NaN' else 'NaN'

    def insert_parameters(self, key, value):
        self.insert_update(self.parameters, key, value)

    def insert_models(self, key, value):
        self.models[key] = value

    def insert_results(self, key, value):
        if key in self.results.keys():
            self.save_dir = f'{self.save_dir}/fail'
            raise ValueError(f"Key: {key} already exists in ...")
        self.insert_update(self.results, key, value)
    
    def insert_batch_results(self, result_list):
        for result in result_list:
            result_name = retrieve_name(result)
            self.insert_update(self.results, result_name, result)

    def set_description(self, description):
        self.description = description

    def insert_model_parameters(self, key, value):
        if key in self.model_parameters.keys():
            self.save_dir = f'{self.save_dir}/fail'
            raise ValueError(f"Key: {key} already exists...")
        self.insert_update(self.model_parameters, key, value)
    
    def insert_training_parameters(self, key, value):
        if key in self.training_parameters.keys():
            self.save_dir = f'{self.save_dir}/fail'
            raise ValueError(f"Key: {key} already exists...")
        self.insert_update(self.training_parameters, key, value)
    
    def insert_miscellaneous_parameters(self, key, value):
        if key in self.miscellaneous_parameters.keys():
            self.save_dir = f'{self.save_dir}/fail'
            raise ValueError(f"Key: {key} already exists...")
        self.insert_update(self.miscellaneous_parameters, key, value)
    
    def insert_data_parameters(self, key, value):
        if key in self.data_parameters.keys():
            self.save_dir = f'{self.save_dir}/fail'
            raise ValueError(f"Key: {key} already exists...")
        self.insert_update(self.data_parameters, key, value)
    
    def get_model_parameter_by_key(self, key):
        return self.model_parameters[key]
    
    def get_training_parameter_by_key(self, key):
        return self.training_parameters[key]
    
    def get_miscellaneous_parameter_by_key(self, key):
        return self.miscellaneous_parameters[key]

    def get_data_parameter_by_key(self, key):
        return self.data_parameters[key]

    def delete_model_parameter_by_key(self, key):
        self.model_parameters.pop(key)

    def delete_training_parameter_by_key(self, key):
        self.training_parameters.pop(key)

    def delete_miscellaneous_parameter_by_key(self, key):
        self.miscellaneous_parameters.pop(key)

    def delete_data_parameter_by_key(self, key):
        self.data_parameters.pop(key) 

    def update_model_parameter_by_key(self, key, value):
        self.insert_update(self.model_parameters, key, value)

    def update_training_parameter_by_key(self, key, value):
        self.insert_update(self.training_parameters, key, value)

    def update_miscellaneous_parameter_by_key(self, key, value):
        self.insert_update(self.miscellaneous_parameters, key, value)
    
    def update_data_parameter_by_key(self, key, value):
        self.insert_update(self.data_parameters, key, value)
    
    def insert_batch_model_parameters(self, parameter_list):
        for param in parameter_list:
            param_name = retrieve_name(param)
            self.insert_model_parameters(param_name, param)
    
    def insert_batch_training_parameters(self, parameter_list):
        for param in parameter_list:
            param_name = retrieve_name(param)
            self.insert_training_parameters(param_name, param)
    
    def insert_batch_miscellaneous_parameters(self, parameter_list):
        for param in parameter_list:
            param_name = retrieve_name(param)
            self.insert_miscellaneous_parameters(param_name, param)

    def insert_batch_data_parameters(self, parameter_list):
        for param in parameter_list:
            param_name = retrieve_name(param)
            self.insert_data_parameters(param_name, param)
    
    def update_batch_model_parameters(self, parameter_list):
        for param in parameter_list:
            param_name = retrieve_name(param)
            self.update_model_parameter_by_key(param_name, param)
    
    def update_batch_training_parameters(self, parameter_list):
        for param in parameter_list:
            param_name = retrieve_name(param)
            self.update_training_parameter_by_key(param_name, param)
    
    def update_batch_miscellaneous_parameters(self, parameter_list):
        for param in parameter_list:
            param_name = retrieve_name(param)
            self.update_miscellaneous_parameter_by_key(param_name, param)
    
    def update_batch_data_parameters(self, parameter_list):
        for param in parameter_list:
            param_name = retrieve_name(param)
            self.update_data_parameter_by_key(param_name, param)


if __name__ == '__main__':
    x = ParameterWatcher('test')
    epoch = 1
    lr = 0.01
    params = [epoch, lr]
    x.insert_batch_model_parameters(params)
    print(x.model_parameters)