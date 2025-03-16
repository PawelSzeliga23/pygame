import pygame as pg
import time


class Timer:
    def __init__(self, game):
        self.game = game
        self.current_time = 0
        self.font = pg.font.Font(None, 30)

    def update(self):
        self.current_time = time.time()

    def start(self):
        self.start_time = time.time()

    def draw(self):
        text = self.font.render(str(round(self.current_time - self.start_time, 2)), True, 'white')
        self.game.screen.blit(text, (10, 10))

    @property
    def time(self):
        return round(self.current_time - self.start_time, 2)
