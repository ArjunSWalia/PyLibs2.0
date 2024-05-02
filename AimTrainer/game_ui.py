import pygame
from config import Config
from utils import format_time, get_middle

class GameUI:
    def __init__(self, win):
        self.win = win
        self.label_font = pygame.font.SysFont(Config.LABEL_FONT_NAME, Config.LABEL_FONT_SIZE)

    def draw_top_bar(self, elapsed_time, targets_pressed, misses):
        pygame.draw.rect(self.win, pygame.Color("grey"), (0, 0, Config.WIDTH, Config.TOP_BAR_HEIGHT))
        self._draw_labels(elapsed_time, targets_pressed, misses)

    def _draw_labels(self, elapsed_time, targets_pressed, misses):
        time_label = self.label_font.render(f"Time: {format_time(elapsed_time)}", True, pygame.Color("black"))
        speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
        speed_label = self.label_font.render(f"Speed: {speed} t/s", True, pygame.Color("black"))
        hits_label = self.label_font.render(f"Hits: {targets_pressed}", True, pygame.Color("black"))
        lives_label = self.label_font.render(f"Lives: {Config.LIVES - misses}", True, pygame.Color("black"))

        self.win.blit(time_label, (5, 5))
        self.win.blit(speed_label, (200, 5))
        self.win.blit(hits_label, (450, 5))
        self.win.blit(lives_label, (650, 5))

    def end_screen(self, elapsed_time, targets_pressed, clicks):
        self.win.fill(Config.BG_COLOR)
        accuracy = round(targets_pressed / clicks * 100, 1) if clicks > 0 else 0

        labels = [
            ("Time: " + format_time(elapsed_time), pygame.Color("white")),
            (f"Speed: {round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0} t/s", pygame.Color("white")),
            (f"Hits: {targets_pressed}", pygame.Color("white")),
            (f"Accuracy: {accuracy}%", pygame.Color("white"))
        ]

        for i, (text, color) in enumerate(labels):
            label = self.label_font.render(text, True, color)
            self.win.blit(label, (get_middle(label, Config.WIDTH), 100 + i * 100))

        pygame.display.update()
        self._wait_for_exit()

    def _wait_for_exit(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    quit()
