import pygame
import math
import numpy as np
from numba import njit

@njit(fastmath=True)
def ray_casting(screen_array, player_pos, player_angle, player_height,
                player_pitch, screen_width, screen_height, delta_angle, ray_distance, h_fov, scale_height, map_width, map_height, height_map, color_map):

    screen_array[:] = np.array([0,0,0])
    y_buffer = np.full(screen_width, screen_height)

    ray_angle = player_angle - h_fov
    for ray in range(screen_width):
        first_ray_contact = True # to handle infinite lines going down
        sin_r = math.sin(ray_angle)
        cos_r = math.cos(ray_angle)

        for depth in range(1, ray_distance):
            x = int(player_pos[0] + depth*cos_r)
            if 0 < x < map_width:
                y = int(player_pos[1] + depth*sin_r)
                if 0 < y < map_height:
                    depth *= math.cos(player_angle - ray_angle) # remove fish-eye
                    height_on_screen = int((player_height - height_map[x,y][0]) / depth*scale_height + player_pitch)

                    # remove unnecessary drawing
                    if first_ray_contact:
                        y_buffer[ray] = min(height_on_screen, screen_height)
                        first_ray_contact = False

                    # remove mirror bug
                    if height_on_screen < 0:
                        height_on_screen = 0

                    # draw vertical line
                    if height_on_screen < y_buffer[ray]:
                        for screen_y in range(height_on_screen, y_buffer[ray]):
                            screen_array[ray,screen_y] = color_map[x,y]
                        y_buffer[ray] = height_on_screen

        ray_angle += delta_angle
    return screen_array

class Renderer:
    def __init__(self, app):
        self.app = app
        self.player = app.player
        self.fov = math.pi / 3
        self.h_fov = self.fov / 2
        self.num_rays = app.width
        self.delta_angle = self.fov / self.num_rays
        self.ray_distance = 2000
        self.scale_height = 620
        self.screen_array = np.full((app.width,app.height,3), (0,0,0))
        self.maps = self.load_maps()
        self.current_map = 'pyramid'
        self.map_width = len(self.maps[self.current_map][0])
        self.map_height = len(self.maps[self.current_map][0][0])
        self.height_map = self.maps[self.current_map][0]
        self.color_map = self.maps[self.current_map][1]

    def load_maps(self):
         return {
                'pyramid':
                (pygame.surfarray.array3d(pygame.image.load('assets/H_pyramid.png')), pygame.surfarray.array3d(pygame.image.load('assets/C_pyramid.png'))),
                'desert':
                (pygame.surfarray.array3d(pygame.image.load('assets/H_desert.png')), pygame.surfarray.array3d(pygame.image.load('assets/C_desert.png'))),
                'snow':
                (pygame.surfarray.array3d(pygame.image.load('assets/H_snow.png')), pygame.surfarray.array3d(pygame.image.load('assets/C_snow.png'))),
                'lava':
                (pygame.surfarray.array3d(pygame.image.load('assets/H_lava.png')), pygame.surfarray.array3d(pygame.image.load('assets/C_lava.png'))),
                'swamp':
                (pygame.surfarray.array3d(pygame.image.load('assets/H_swamp.png')), pygame.surfarray.array3d(pygame.image.load('assets/C_swamp.png'))),
                'boulder':
                (pygame.surfarray.array3d(pygame.image.load('assets/H_boulder.png')), pygame.surfarray.array3d(pygame.image.load('assets/C_boulder.png'))),
                'crater':
                (pygame.surfarray.array3d(pygame.image.load('assets/H_crater.png')), pygame.surfarray.array3d(pygame.image.load('assets/C_crater.png'))),
                'snow2':
                (pygame.surfarray.array3d(pygame.image.load('assets/H_snow2.png')), pygame.surfarray.array3d(pygame.image.load('assets/C_snow2.png')))
                }
         
    def update_current_map(self, chosen_map):
        self.current_map = chosen_map
        self.map_width = len(self.maps[self.current_map][0])
        self.map_height = len(self.maps[self.current_map][0][0])
        self.height_map = self.maps[self.current_map][0]
        self.color_map = self.maps[self.current_map][1]

    def update(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_0]:
            self.update_current_map('pyramid')
        if pressed_key[pygame.K_1]:
            self.update_current_map('desert')
        if pressed_key[pygame.K_2]:
            self.update_current_map('lava')
        if pressed_key[pygame.K_3]:
            self.update_current_map('snow')
        if pressed_key[pygame.K_4]:
            self.update_current_map('crater')
        if pressed_key[pygame.K_5]:
            self.update_current_map('swamp')
        if pressed_key[pygame.K_6]:
            self.update_current_map('boulder')
        if pressed_key[pygame.K_7]:
            self.update_current_map('snow2')

        self.screen_array = ray_casting(self.screen_array, self.player.pos, self.player.angle,
                                        self.player.height, self.player.pitch, self.app.width, 
                                        self.app.height, self.delta_angle, self.ray_distance, self.h_fov,
                                        self.scale_height, self.map_width, self.map_height,
                                        self.height_map, self.color_map)

    def draw(self):
        self.app.screen.blit(pygame.surfarray.make_surface(self.screen_array), (0,0))