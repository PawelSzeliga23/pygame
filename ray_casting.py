import pygame as pg
import math
from Settings import *


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_res = []
        self.objects_to_render = []
        self.textures = self.game.objects.walls

    def get_objects_to_render(self):
        self.objects_to_render.clear()
        for ray, value in enumerate(self.ray_casting_res):
            depth, height, texture, offset = value

            if height < HEIGHT:
                wall_column = self.textures[texture].subsurface(offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE)
                wall_column = pg.transform.scale(wall_column, (SCALE, height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / height
                wall_column = self.textures[texture].subsurface(offset * (TEXTURE_SIZE - SCALE),
                                                                HALF_TEXTURE_SIZE - texture_height // 2, SCALE,
                                                                texture_height)
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_res.clear()
        ox, oy = self.game.player.pos()
        x_maze, y_maze = self.game.player.map_pos()

        texture_v, texture_h = 1, 1

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(RAYS_NUMBER):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            y_hor, dy = (y_maze + 1, 1) if sin_a > 0 else (y_maze - 1e-6, -1)
            depth_h = (y_hor - oy) / sin_a
            x_hor = ox + depth_h * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a
            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.maze.world:
                    texture_h = self.game.maze.world[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_h += delta_depth

            x_vert, dx = (x_maze + 1, 1) if cos_a > 0 else (x_maze - 1e-6, -1)
            depth_v = (x_vert - ox) / cos_a
            y_vert = oy + depth_v * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.maze.world:
                    texture_v = self.game.maze.world[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_v += delta_depth

            if depth_v < depth_h:
                depth, texture = depth_v, texture_v
                y_vert %= 1
                offset = y_vert if cos_a > 0 else 1 - y_vert
            else:
                depth, texture = depth_h, texture_h
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            depth *= math.cos(self.game.player.angle - ray_angle)

            projection_height = SCREEN_DIST / (depth + 1e-6)

            self.ray_casting_res.append((depth, projection_height, texture, offset))

            # color = [255 / (1 + depth ** 9 * 0.00002)] * 3

            # pg.draw.rect(self.game.screen, color,
            #              (ray * SCALE, HALF_HEIGHT - projection_height // 2, SCALE, projection_height))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()
