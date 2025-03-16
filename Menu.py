import sys

import pygame as pg
from Settings import *


class Menu:
    def __init__(self, game, name, menu_items):
        self.game = game
        self.font = pg.font.Font(None, 50)
        self.menu_font = pg.font.Font(None, 100)
        self.menu_name = name
        self.menu_items = menu_items
        self.start_rect = pg.Rect(HALF_WIDTH - 100, 300, 200, 50)
        self.quit_rect = pg.Rect(HALF_WIDTH - 100, 400, 200, 50)
        self.text_rect = pg.Rect(HALF_WIDTH - 100, 500, 200, 50)
        self.surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        self.text_active = False

    def draw(self):
        self.surface.fill((0, 0, 0, 60))
        self.game.screen.blit(self.surface, (0, 0))
        text = self.menu_font.render(self.menu_name, True, 'white')
        rect = pg.Rect(HALF_WIDTH - 250, 100, 500, 100)
        pg.draw.rect(self.game.screen, (45, 45, 45), rect)
        pg.draw.rect(self.game.screen, 'white', rect, 2)
        self.game.screen.blit(text, (HALF_WIDTH - 100, 110))
        for i, item in enumerate(self.menu_items):
            text = self.font.render(item, True, 'white')
            rect = pg.Rect(HALF_WIDTH - 100, 300 + i * 100, 200, 50)
            pg.draw.rect(self.game.screen, (45, 45, 45), rect)
            pg.draw.rect(self.game.screen, 'white', rect, 2)
            self.game.screen.blit(text, (HALF_WIDTH - 90, 310 + i * 100))
        self.draw_textfield(pg.Rect(HALF_WIDTH - 100, 500, 200, 50), 'Enter your name', self.text_active)
        text = self.font.render(self.game.player_name, True, (255, 255, 255))
        self.game.screen.blit(text, (HALF_WIDTH - 100, 510))
        self.game.highscore.draw()

    def draw_textfield(self, rect, text, active):
        color = (0, 100, 255) if active else (45, 45, 45)
        pg.draw.rect(self.game.screen, color, rect, 0)
        pg.draw.rect(self.game.screen, (255, 255, 255), rect, 2)

        font = pg.font.Font(None, 20)
        text_surface = font.render(text, True, (255, 255, 255))
        self.game.screen.blit(text_surface, (rect.x + 5, rect.y + 5))

    def update(self):
        if not self.game.menu_bool:
            return

    def check_events(self, event):
        if pg.mouse.get_pressed()[0]:
            if self.start_rect.collidepoint(pg.mouse.get_pos()):
                self.game.new_game()
                self.game.menu_bool = False
                self.game.freeze = False
                self.game.mouse = False
                pg.mouse.set_visible(False)
            if self.quit_rect.collidepoint(pg.mouse.get_pos()):
                self.game.highscore.save()
                pg.quit()
                sys.exit()
            if self.text_rect.collidepoint(pg.mouse.get_pos()):
                self.text_active = True
        if self.text_active:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.text_active = False
                elif event.key == pg.K_BACKSPACE:
                    self.game.player_name = self.game.player_name[:-1]
                else:
                    if len(self.game.player_name) < 10:
                        self.game.player_name += event.unicode
