class Config:
    def __init__(self):
        self.config = {
            'port': 8080,
            'host': 'localhost',
            'threads': [],
            'metrics': {
                'cpu_percent': 0,
                'memory_available': 0,
                'bytes_sent': 0
            },
            'prometheus_port': 8000
        }

    def get_config(self, key):
        return self.config[key]

    def set_config(self, key, value):
        self.config[key] = value
