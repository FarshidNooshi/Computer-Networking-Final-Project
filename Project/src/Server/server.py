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
        global s
        run_prometheus(self.config.get_config('prometheus_port'))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            while True:
                s.listen(1)
                conn, (ip, port) = s.accept()
                client = ClientHandler(conn)
                print(f'Connected by, {ip}:{port}')
                client.start()
                self.threads.append(client)
        except Exception as e:
            print(e)
        finally:
            s.close()

        for item in self.threads:
            item.conn.close()
            item.join()


def run_prometheus(port):
    start_http_server(port)


if __name__ == '__main__':
    server = Server()
    server.run()
