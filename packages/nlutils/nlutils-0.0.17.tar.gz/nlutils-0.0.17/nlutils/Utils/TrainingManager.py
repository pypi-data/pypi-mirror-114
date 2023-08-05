import os
import subprocess
from multiprocessing import Process, Queue, Lock, Pool
from .Log import Logger
from .Exception import *
from abc import abstractmethod, ABCMeta

class Strategy(ABCMeta):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = cls.__new__(cls, *args, **kwargs)
        return cls.instance
    
    @abstractmethod
    def run(self, *args, **kwargs):
        pass

class DeviceLoad(Strategy):

    def run(self, **kwargs):
        server_infos = kwargs.get('server_infos')
        task_infos = kwargs.get('task_infos')
        # TODO implement more logic here


def get_all_device_memory():
    cmd = "nvidia-smi | grep MiB | awk '{print $9  $11}' | grep -v '|'"
    device_memories = subprocess.getoutput(cmd).split("\n")
    if 'command not found' in device_memories[0]:
        raise CUDANotFoundException("\033[;91;1mCUDA is not found in current environment.\033[0m")
    device_infos = list()
    for device_id, device_memory in enumerate(device_memories):
        device_used_memory = int(device_memory.split("MiB")[0])
        device_total_memory = int(device_memory.split("MiB")[1])
        device_available_memory = device_total_memory - device_used_memory
        device_available_memory_precent = device_available_memory / device_total_memory
        device_info = {'device_id': device_id, 'device_total_memory':device_total_memory, 'device_available_memory': device_available_memory, 'device_used_memory':device_used_memory, 'device_available_memory_precent': device_available_memory_precent}
        device_infos.append(device_info)
    return device_infos

def device_load_balance(precent_threshold=0.4, memory_threshold=12000):
    device_infos = get_all_device_memory()
    device_infos.sort(key=lambda x:x['device_available_memory'], reverse=True)
    selected_devices_ids = []
    for device_info in device_infos:
        if device_info['device_available_memory_precent'] >= precent_threshold or device_info['device_available_memory'] >= memory_threshold:
            selected_devices_ids.append(device_info['device_id'])
    if selected_devices_ids.__len__() == 0:
        raise DeviceNotAvailableException("\033[;91;1mNo Device can be used for now.\033[0m")
    return selected_devices_ids

def get_available_device_ids(precent_threshold=0.4, memory_threshold=12000):
    selected_devices_ids = device_load_balance(precent_threshold)
    idx = 0
    while True:
        yield selected_devices_ids[idx]
        idx = idx + 1 if idx < len(selected_devices_ids) - 1 else 0


class TrainingManager(object):

    def __init__(self):
        pass

    @staticmethod
    def shell_training(cmd_str):
        Logger.get_logger().info(f"Process {os.getpid()} is running")
        os.system(cmd_str)

    def start_shell_training(self, cmd_strs):
        self.training_pool = Pool(len(cmd_strs))
        self.training_pool.map(TrainingManager.shell_training, cmd_strs)
        self.training_pool.close()
        self.training_pool.join()
    
    def start_api_training(self, entry, arg_list):
        self.training_pool = Pool(arg_list)
        self.training_pool.map(entry, arg_list)
        self.training_pool.close()
        self.training_pool.join()

