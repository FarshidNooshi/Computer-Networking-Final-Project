import json
import sys
from threading import Thread

from prometheus_client import Gauge, Counter


class ClientHandler(Thread):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        name = self.conn.recv(1024).decode()
        print(f'client name is {name}')
        self.cpu = Gauge(f'cpu_usagepercent{name}', 'percentage of cpu usage right now.')
        self.mem = Gauge(f'memavailable{name}', 'available memory in bytes.')
        self.net = Counter(f'network_usagetotal{name}', 'total number of received bytes.')
        self.client_net = Counter(f'network_sendtotal{name}', 'total number of send bytes.')

    def run(self):
        while True:
            print('waiting for data')
            data = self.conn.recv(1024)
            sz = sys.getsizeof(data)
            if not data:
                continue
            data = data.decode()
            metrics = json.loads(data)
            self.cpu.set(metrics['cpu_percent'])
            self.net.inc(sz)
            self.mem.set(metrics['memory_available'])
            self.client_net.inc(metrics['bytes_sent'])
            print(f'metrics are: {metrics}')
            print(f'size of data is: {sz}')