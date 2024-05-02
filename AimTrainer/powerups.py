import random
from target import Target

class PowerUp(Target):
    TYPES = ['extra_life', 'slow_motion', 'score_multiplier']

    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = random.choice(self.TYPES)
        self.applied = False  
    def apply_effect(self, game_state):
        """Apply the power-up effect based on its type."""
        if self.type == 'extra_life' and not self.applied:
            game_state['lives'] += 1
            self.applied = True
        elif self.type == 'slow_motion' and not self.applied:
            game_state['slow_motion'] = True
            self.applied = True
        elif self.type == 'score_multiplier' and not self.applied:
            game_state['score_multiplier'] *= 2
            self.applied = True

    def draw(self, win):
        super().draw(win) 