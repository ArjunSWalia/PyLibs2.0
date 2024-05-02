import json

class ConfigLoader:
    DEFAULT_PATH = "game_config.json"

    @staticmethod
    def load_config(path=None):
        if path is None:
            path = ConfigLoader.DEFAULT_PATH
        with open(path, 'r') as file:
            return json.load(file)
