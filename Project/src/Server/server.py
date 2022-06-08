import socket

from prometheus_client import start_http_server

from src.Server.Utils.ClientHandler import ClientHandler
from src.Server.Utils.config import Config


class Server:
    def __init__(self):
        self.config = Config()
        self.port = self.config.get_config('port')
        self.host = self.config.get_config('host')
        self.threads = self.config.get_config('threads')
        self.metrics = self.config.get_config('metrics')

    def run(self):
        run_prometheus(self.config.get_config('prometheus_port'))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            conn, (ip, port) = s.accept()
            with ClientHandler(conn) as client:
                print(f'Connected by, {ip}:{port}')
                client.start()
                self.threads.append(client)

        for item in self.threads:
            item.conn.close()
            item.join()


def run_prometheus(port):
    start_http_server(port)


if __name__ == '__main__':
    server = Server()
    server.run()
