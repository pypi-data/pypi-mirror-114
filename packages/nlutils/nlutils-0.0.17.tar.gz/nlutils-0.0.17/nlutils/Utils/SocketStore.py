import time
import json
import socket

from nlutils.Utils.Log import default_logger

class SocketSenderProxy(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SocketSenderProxy, cls).__new__(cls, *args, **kwargs)
        return cls.instance
    
    def create_pkg(self, msg_dict):
        msg_dict['timestamp'] = time.time()
        return msg_dict
    
    def seralize(self, pkg):
        return pkg.__str__().replace("'", '"').encode("utf-8")
        
    def send(self, host, port, msg) -> bool:
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect((host, port))
        try:
            msg = self.create_pkg(self, msg)
            buffer = self.seralize(msg)
            self.socket.sendall(buffer)
            self.socket.close()
            return True
        except (socket.error, BrokenPipeError, OSError):
            default_logger.error("Send failed, cannot connect to server.")
            return False
        except Exception as e:
            default_logger.error(f"Send failed, unknown failure: {str(e)}.")
            return False

class AITaskSenderProxy(SocketSenderProxy):

    def __init__(self, ai_server_ip, ai_server_port):
        self.ai_server_ip = ai_server_ip
        self.ai_server_port = ai_server_port
    
    def send(self, task):
        pass


if __name__ == '__main__':
    x = {
        'asdasfa': "afasfas"
    }
