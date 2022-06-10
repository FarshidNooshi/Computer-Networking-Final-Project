from os import path

import json


class Config:
    def __init__(self):
        file_path = path.join(path.dirname(__file__), 'json', 'data.json')
        with open(file_path) as json_file:
            data = json.load(json_file)
            self.config = data

    def get_config(self, key):
        return self.config[key]

    def set_config(self, key, value):
        self.config[key] = value


# import json
if __name__ == '__main__':
    config = Config()
    print(config.get_config('port'))
