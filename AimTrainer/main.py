import pygame
import random
import time
from datetime import datetime
from target import Target
from game_ui import GameUI
from config import Config
from difficulty_adjuster import DifficultyAdjuster
from ai_predictor import AIPredictor
from physics_engine import TargetPhysics
from high_score_client import HighScoreClient

class MainGame:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption("Aim Trainer")
        self.clock = pygame.time.Clock()
        self.game_ui = GameUI(self.win)
        self.targets = []
        self.start_time = time.time()
        self.targets_pressed = 0
        self.clicks = 0
        self.misses = 0
        self.difficulty_adjuster = DifficultyAdjuster()
        self.ai_predictor = AIPredictor()
        self.physics = TargetPhysics()
        self.high_score_client = HighScoreClient()
        pygame.time.set_timer(pygame.USEREVENT + 1, Config.TARGET_INCREMENT)
        self.running = True
        self.score = 0

    def log_event(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def run(self):
        while self.running:
            click = False
            elapsed_time = time.time() - self.start_time
            self.handle_events()

            self.update_targets(click)
            self.game_ui.draw_top_bar(elapsed_time, self.targets_pressed, self.misses)

            if self.misses >= Config.LIVES:
                self.handle_game_over(elapsed_time)

            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.USEREVENT + 1:
                self.add_target()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(mouse_pos)

    def handle_click(self, mouse_pos):
        self.clicks += 1
        self.update_targets(True, mouse_pos)
        self.log_event("Mouse click registered.")

    def add_target(self):
        x, y = self.ai_predictor.predict_next_click() or (random.randint(Config.TARGET_PADDING, Config.WIDTH - Config.TARGET_PADDING),
                                                          random.randint(Config.TARGET_PADDING + Config.TOP_BAR_HEIGHT, Config.HEIGHT - Config.TARGET_PADDING))
        new_target = Target(x, y)
        self.targets.append(new_target)
        self.log_event("New target added.")

    def update_targets(self, click, mouse_pos=None):
        for target in self.targets[:]:
            target.update()
            target.draw(self.win)
            if target.size <= 0:
                self.targets.remove(target)
                self.misses += 1
            elif click and mouse_pos and target.collide(*mouse_pos):
                self.process_target_hit(target)
                self.ai_predictor.update_history(mouse_pos)

    def process_target_hit(self, target):
        self.targets_pressed += 1
        self.score += 100 - int(target.size)  # Example scoring mechanism
        self.targets.remove(target)
        self.log_event("Target hit.")

    def handle_game_over(self, elapsed_time):
        self.running = False
        self.game_ui.end_screen(elapsed_time, self.targets_pressed, self.clicks)
        self.submit_high_score()
        self.log_event("Game over.")

    def submit_high_score(self):
        name = input("Enter name: ")
        self.high_score_client.submit_score(name, self.score)
        self.log_event("High score submitted.")

    def adjust_difficulty_based_on_performance(self):
        if self.targets_pressed % 10 == 0:  # Every 10 hits, possibly adjust difficulty
            new_difficulty = self.difficulty_adjuster.adjust(self.score)
            self.log_event(f"Difficulty adjusted to {new_difficulty}.")

if __name__ == "__main__":
    game = MainGame()
    game.run()
