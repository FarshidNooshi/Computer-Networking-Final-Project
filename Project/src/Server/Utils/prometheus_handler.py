from prometheus_client import start_http_server


class PrometheusHandler:
    def __init__(self):
        pass

    @staticmethod
    def run_prometheus(port):
        start_http_server(port)
