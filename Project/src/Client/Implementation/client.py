import json
import socket
from time import sleep

import psutil

from src.Business.config import Config
from src.Business.log.logger import MyLogger


class Client:
    def __init__(self, client_name):
        self.config = Config()
        self.server_port = self.config.get_config('port')
        self.server_host = self.config.get_config('host')
        self.name = client_name

    def run(self):
        logger = MyLogger('project.client')
        while True:
            sleep(3)
            global s
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.server_host, self.server_port))
                s.sendall(self.name.encode())
                logger.info(f'Client {self.name} connected to server')
                while True:
                    if s.connect_ex((self.server_host, self.server_port)) == 0:
                        logger.error(f'Client {self.name} disconnected')
                        break
                    values = self.create_metrics()
                    encoded_values = json.dumps(values).encode()
                    s.sendall(encoded_values)
                    logger.info(f'Client {self.name} sent metrics')
            except Exception as e:
                logger.error(f'Client {self.name} error: {e}')
            finally:
                s.close()

    @staticmethod
    def create_metrics():
        metrics = {
            'cpu_utilization_percent': psutil.cpu_percent(interval=1),
            'memory_available': psutil.virtual_memory().available,
            'num_bytes_sent': psutil.net_io_counters().bytes_sent,
            'num_errors_recv': psutil.net_io_counters().errin,
        }
        return metrics
