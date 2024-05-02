import random

class LevelGenerator:
    def generate_level(difficulty):
        level_config = {
            'target_speed': random.randint(1, difficulty),
            'target_size': max(10, 30 - difficulty),
            'spawn_rate': 2000 - difficulty * 100
        }
        return level_config
