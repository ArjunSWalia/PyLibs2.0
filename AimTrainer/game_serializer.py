import json

class GameStateSerializer:
    @staticmethod
    def save_game_state(file_path, game_state):
        with open(file_path, 'w') as file:
            json.dump(game_state, file)

    @staticmethod
    def load_game_state(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
