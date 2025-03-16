import Settings
from Menu import Menu
from Settings import *
import pygame as pg
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POSITIONS
        self.angle = PLAYER_ANGLE
        self.speed = PLAYER_SPEED
        self.rotation = PLAYER_ROTATION
        self.durability = 400

    def move(self):
        if self.game.freeze:
            return
        keys = pg.key.get_pressed()
        if keys[pg.K_LSHIFT] and self.durability > 0:
            speed = 1.8 * PLAYER_SPEED * self.game.dt
            self.durability -= 0.7
        else:
            speed = PLAYER_SPEED * self.game.dt
            if self.durability < 400:
                self.durability += 0.5
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed_sin = sin_a * speed
        speed_cos = cos_a * speed

        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx -= speed_cos
            dy -= speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy -= speed_cos
        if keys[pg.K_d]:
            dx -= speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROTATION * self.game.dt
        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROTATION * self.game.dt
        self.angle %= 2 * math.pi

    def update(self):
        self.move()
        self.mouse_control()

    def draw(self):
        scale = self.game.maze.minimap_scale
        x, y = self.game.maze.minimap_x, self.game.maze.minimap_y
        pg.draw.line(self.game.screen, 'yellow', (x + self.x * scale, y + self.y * scale),
                     (x + self.x * scale + 0.5 * math.cos(self.angle) * scale,
                      y + self.y * scale + 0.5 * math.sin(self.angle) * scale), 2)
        pg.draw.circle(self.game.screen, 'green', (x + self.x * scale, y + self.y * scale), 0.20 * scale)

    def pos(self):
        return self.x, self.y

    def map_pos(self):
        return int(self.x), int(self.y)

    def check_wall(self, x, y):
        return (x, y) not in self.game.maze.world

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE / self.game.dt
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy
        if self.check_win():
            self.game.menu = Menu(self.game, 'You win!', ['Next Level', 'Quit'])
            self.game.menu_bool = True
            self.game.freeze = True
            self.game.mouse = True
            self.game.map_height += 2
            self.game.map_width += 2
            pg.mouse.set_visible(True)
            self.game.score.update()

    def mouse_control(self):
        if self.game.freeze:
            return
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENS * self.game.dt

    def check_win(self):
        # print(self.map_pos())
        # print('Maze')
        # print(self.game.maze.end_game_pos)
        return self.map_pos() == self.game.maze.end_game_pos
