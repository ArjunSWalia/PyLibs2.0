class ScoringSystem:
    def __init__(self):
        self.score = 0

    def calculate_score(self, target, reaction_time):
        size_score = 100 - target.size 
        time_score = max(0, 100 - reaction_time * 10) 
        self.score += size_score + time_score
