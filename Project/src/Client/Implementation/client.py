import json
import socket

import psutil

from src.Server.Utils.config import Config


class Client:
    def __init__(self, client_name):
        self.config = Config()
        self.server_port = self.config.get_config('port')
        self.server_host = self.config.get_config('host')
        self.name = client_name

    def run(self):
        global s
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.server_host, self.server_port))
            s.sendall(self.name.encode())
            print('connected')
            while True:
                values = self.gather_metrics()
                encoded_values = json.dumps(values).encode()
                s.sendall(encoded_values)
                print('here from client')
        except Exception as e:
            print(e)
        finally:
            s.close()

    @staticmethod
    def gather_metrics():
        metrics = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_available': psutil.virtual_memory().available,
            'bytes_sent': psutil.net_io_counters().bytes_sent
        }
        return metrics
