import pygame as pg
from Settings import *


class ObjectRenderer():
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.walls = self.load_walls()
        self.durability_back_rect = pg.Rect(10, HEIGHT - 60, 410, 50)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert()
        return pg.transform.scale(texture, res)

    def load_walls(self):
        return {
            1: self.get_texture('resources/textures/Brick_01_512.png'),
            2: self.get_texture('resources/textures/Brick_01_512Moss.png'),
            3: self.get_texture('resources/textures/Brick_01_512Grafity.png'),
            4: self.get_texture('resources/textures/Brick_01_512Start.png'),
            5: self.get_texture('resources/textures/Brick_01_512end.png'),
        }

    def render_objects(self):
        object_list = self.game.ray_casting.objects_to_render
        for depth, image, pos in object_list:
            self.screen.blit(image, pos)
        durability_rect = self.get_durability_rect()
        pg.draw.rect(self.screen, 'white', self.durability_back_rect)
        pg.draw.rect(self.screen, 'blue', durability_rect)

    def draw(self):
        self.draw_background()
        self.render_objects()

    def draw_background(self):
        pg.draw.rect(self.screen, (45, 45, 45), (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def get_durability_rect(self):
        return pg.Rect(15, HEIGHT - 55, self.game.player.durability, 40)
