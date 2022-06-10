import socket
import threading
from time import sleep

from src.Business.log.logger import MyLogger
from src.Server.Utils.ClientHandler import ClientHandler
from src.Business.config import Config
from src.Server.Utils.prometheus_handler import PrometheusHandler


class Server:
    def __init__(self):
        self.threads = []
        self.config = Config()
        self.port = self.config.get_config('port')
        self.host = self.config.get_config('host')
        self.metrics = self.config.get_config('metrics')
        self.lock = threading.Lock()
        PrometheusHandler().run_prometheus(self.config.get_config('prometheus_port'))

    def run(self):
        logger = MyLogger('project.server')
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)
        logger.info(f'Server started on {self.host}:{self.port}')
        try:
            while True:
                conn, addr = s.accept()
                self.lock.acquire()
                client_handler = ClientHandler(conn, self.lock)
                logger.info(f'Client {addr} connected to server')
                client_handler.start()
                self.threads.append(client_handler)
        except Exception as e:
            logger.error(f'Server error: {e}')
        finally:
            s.close()
            for item in self.threads:
                item.conn.close()
                item.join()
