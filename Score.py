import pygame as pg
from Settings import *


class Score:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.Font(None, 40)
        self.score = 0

    def update(self):
        time = self.game.timer.time
        max_points = self.game.map_width * self.game.map_height
        self.score += round(max_points - time * 1.5)

    def draw(self):
        score = "Score: " + str(self.score)
        score_len = len(score)
        text = self.font.render(score, True, 'white')
        self.game.screen.blit(text, (WIDTH - 10 - score_len * 14, 10))
