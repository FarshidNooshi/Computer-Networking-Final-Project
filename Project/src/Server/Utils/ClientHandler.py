import json
import sys
from threading import Thread

from prometheus_client import Gauge, Counter

from src.Business.log.logger import logging_decorator, MyLogger


class ClientHandler(Thread):
    def __init__(self, conn, lock):
        super().__init__()
        self.conn = conn
        self.lock = lock
        self.logger = MyLogger('project.server')
        self.name = self.conn.recv(1024).decode()
        self.logger.info(f'Client name is {self.name}')
        self.cpu = None
        self.mem = None
        self.net = None
        self.client_net = None
        self.err_net = None
        self.create_metrics()

    def run(self):
        try:
            while True:
                self.logger.info(f'waiting for data from client {self.name}')
                data = self.conn.recv(1024)
                sz = sys.getsizeof(data)
                if not data:
                    self.logger.info(f'no data received from client {self.name}')
                    self.lock.release()
                    break
                data = data.decode()
                metrics = json.loads(data)
                client_name = f'client_name: {self.name}'
                self.update_metrics(client_name, metrics, sz)
        except Exception as e:
            self.logger.error(f'Client {self.name} error: {e}')

    @logging_decorator('project.server.client_handler')
    def update_metrics(self, client_name, metrics, sz):
        self.cpu.labels(client_name=client_name).set(metrics['cpu_utilization_percent'])
        self.net.labels(client_name=client_name).inc(sz)
        self.mem.labels(client_name=client_name).set(metrics['memory_available'])
        self.client_net.labels(client_name=client_name).inc(metrics['num_bytes_sent'])
        self.err_net.labels(client_name=client_name).inc(metrics['num_errors_recv'])

    def create_metrics(self):
        self.cpu = Gauge(f'cpu_utilization_percent', 'percentage of cpu usage right now.', labelnames=['client_name'])
        self.mem = Gauge(f'memory_available', 'available memory in bytes.', labelnames=['client_name'])
        self.net = Counter(f'network_usage_total', 'total number of received bytes.', labelnames=['client_name'])
        self.client_net = Counter(f'network_send_total', 'total number of send bytes.', labelnames=['client_name'])
        self.err_net = Counter(f'received_error_total', 'total number of errors while receiving.',
                               labelnames=['client_name'])
