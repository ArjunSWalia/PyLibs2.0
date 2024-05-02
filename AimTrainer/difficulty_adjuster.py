class DifficultyAdjuster:
    def __init__(self, game_state):
        self.game_state = game_state

    def adjust_difficulty(self, performance_metric):
        threshold = 3.33  
        adjustment_factor = 0.1  

        if performance_metric > threshold:
            self.game_state['target_increment'] *= (1 - adjustment_factor)
            self.game_state['max_target_size'] *= (1 - adjustment_factor)
        else:
            self.game_state['target_increment'] *= (1 + adjustment_factor)
            self.game_state['max_target_size'] *= (1 + adjustment_factor)
