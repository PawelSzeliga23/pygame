import pygame as pg
import sys
from Settings import *
from maze import Maze
from player import Player
from ray_casting import RayCasting
from object_render import ObjectRenderer
from Menu import Menu
from timer import Timer
from Score import Score
from highscore import HighScoreBoard


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RESOLUTION)
        self.clock = pg.time.Clock()
        self.dt = 1
        self.map_width = MAZE_WIDTH
        self.map_height = MAZE_HEIGHT
        self.score = Score(self)
        self.new_game()
        self.minimap = False
        self.freeze = True
        self.menu_bool = True
        self.mouse = True
        self.player_name = ''
        self.highscore = HighScoreBoard(self)

    def new_game(self):
        self.maze = Maze(self)
        self.player = Player(self)
        self.objects = ObjectRenderer(self)
        self.ray_casting = RayCasting(self)
        self.menu = Menu(self, 'Menu', ['New Game', 'Quit'])
        self.timer = Timer(self)
        self.timer.start()

    def update(self):
        self.timer.update()
        self.menu.update()
        self.maze.update()
        self.player.update()
        self.ray_casting.update()
        pg.display.flip()
        self.dt = self.clock.tick(FPS)
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))

    def check_events(self):
        for event in pg.event.get():
            self.menu.check_events(event)
            if event.type == pg.QUIT:
                self.highscore.save()
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                if self.minimap:
                    self.minimap = not self.minimap
                    self.freeze = not self.freeze
                else:
                    self.menu_bool = not self.menu_bool
                    self.freeze = not self.freeze
                    self.mouse = not self.mouse
                    pg.mouse.set_visible(self.mouse)
            if event.type == pg.KEYDOWN and event.key == pg.K_m:
                if not self.menu_bool:
                    self.minimap = not self.minimap
                    self.freeze = not self.freeze
            self.maze.check_minimap(event)

    def draw(self):
        # self.screen.fill('black')
        self.screen.fill((0, 150, 200))
        if self.minimap:
            self.maze.draw()
            self.player.draw()
            self.timer.draw()
        elif self.menu_bool:
            self.objects.draw()
            self.menu.draw()
        else:
            self.objects.draw()
            self.timer.draw()
        self.score.draw()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
