import pygame as pg
import random
from Settings import *

map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 3, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [2, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 2, 2, 0, 2],
    [2, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [2, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


class Maze:
    def __init__(self, game):
        self.game = game
        self.map = self.generate_maze(game.map_width, game.map_height)
        self.world = {}
        self.create_world()
        self.minimap_x = 0
        self.minimap_y = 0
        self.minimap_scale = MINIMAP_SCALE
        self.minimap_walked = {}
        self.minimap_legend_surface = pg.Surface((200, 200), pg.SRCALPHA)
        self.legend_font = pg.font.Font(None, 30)

    def create_world(self):
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile:
                    self.world[(x, y)] = tile

    def draw(self):
        self.game.screen.fill('black')
        scale = self.minimap_scale
        x, y = self.minimap_x, self.minimap_y
        [pg.draw.rect(self.game.screen, 'gray', (x + pos[0] * scale, y + pos[1] * scale, scale, scale), 2) for pos in
         self.world]
        [pg.draw.rect(self.game.screen, 'red',
                      (x + 10 + pos[0] * scale, y + 10 + pos[1] * scale, scale - 20, scale - 20)) for pos
         in
         self.minimap_walked]
        self.draw_legend()

    def check_minimap(self, event):
        if not self.game.minimap:
            return
        if event.type == pg.MOUSEWHEEL and event.y == 1:
            self.minimap_scale += 10
        if event.type == pg.MOUSEWHEEL and event.y == -1:
            self.minimap_scale -= 10

    def update(self):
        self.minimap_walked[self.game.player.map_pos()] = 1
        if not self.game.minimap:
            return
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.minimap_y += 5
        if keys[pg.K_DOWN]:
            self.minimap_y -= 5
        if keys[pg.K_LEFT]:
            self.minimap_x += 5
        if keys[pg.K_RIGHT]:
            self.minimap_x -= 5

    def draw_legend(self):
        self.minimap_legend_surface.fill((255, 255, 255, 75))
        self.game.screen.blit(self.minimap_legend_surface, (WIDTH - 210, HEIGHT - 210))
        text = self.legend_font.render('LEGEND', True, 'White')
        self.game.screen.blit(text, (WIDTH - 200, HEIGHT - 200))
        text = self.legend_font.render('1. Player', True, 'White')
        self.game.screen.blit(text, (WIDTH - 190, HEIGHT - 170))
        pg.draw.circle(self.game.screen, 'green', (WIDTH - 30, HEIGHT - 160), 7)
        text = self.legend_font.render('2. Walked Path', True, 'White')
        self.game.screen.blit(text, (WIDTH - 190, HEIGHT - 140))
        pg.draw.rect(self.game.screen, 'red', (WIDTH - 35, HEIGHT - 140, 15, 15))

    def generate_maze(self, width=MAZE_WIDTH, height=MAZE_HEIGHT):
        maze = [[1] * width for _ in range(height)]

        def carve_passages(x, y):
            directions = [(x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)]
            random.shuffle(directions)

            for (nx, ny) in directions:
                if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                    maze[ny][nx] = 0
                    maze[(y + ny) // 2][(x + nx) // 2] = 0
                    carve_passages(nx, ny)

        maze[1][1] = 0
        carve_passages(1, 1)

        for i, row in enumerate(maze):
            for j, cell in enumerate(row):
                if cell == 0:
                    continue
                else:
                    value = random.random()
                    if value < 0.1:
                        maze[i][j] = 2
                    if 0.1 < value < 0.11:
                        maze[i][j] = 3
                    if 0.11 < value < 0.36:
                        if i != 0 and i != height - 1 and j != 0 and j != width - 1:
                            maze[i][j] = 0
        maze[1][0] = 4
        rand = random.randint(1, height - 2)
        maze[rand][width - 1] = 5
        if maze[rand][width - 2] == 1:
            maze[rand][width - 2] = 0
        self.end_game_pos = (width - 2, rand)
        # [print(row) for row in maze]

        return maze
