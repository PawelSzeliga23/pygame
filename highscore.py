import pygame as pg
from Settings import *
from score_save import Saver


class HighScoreBoard:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.Font(None, 30)
        self.saver = Saver('highscores.txt')
        self.scores = self.load_scores()
        self.surface = pg.Surface((200, 200), pg.SRCALPHA)

    def load_scores(self):
        scores = self.saver.load()
        scores.sort(key=lambda x: int(x.split(':')[-1]), reverse=True)
        return scores

    def draw(self):
        self.surface.fill((255, 255, 255, 75))
        self.game.screen.blit(self.surface, (WIDTH - 210, HEIGHT - 210))
        text = self.font.render('HIGHSCORE', True, 'White')
        self.game.screen.blit(text, (WIDTH - 200, HEIGHT - 200))
        for i, text in enumerate(self.scores):
            text = self.font.render(str(i + 1) + ". " + text.strip(), True, 'White')
            self.game.screen.blit(text, (WIDTH - 200, HEIGHT - 150 + i * 20))

    def save(self):
        name = self.game.player_name
        score = self.game.score.score
        self.saver.save(score, name)
