import pygame
import math
import numpy as np

class Player:
    def __init__(self):
        self.x = self.y = 0
        self.pos = np.array([self.x,self.y])
        self.angle = math.pi / 4
        self.height = 500
        self.pitch = 40
        self.angle_velocity = 0.01
        self.velocity = 3

    def update(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_UP]:
            self.pitch += self.velocity
        if pressed_key[pygame.K_DOWN]:
            self.pitch -= self.velocity

        if pressed_key[pygame.K_RIGHT]:
            self.angle += self.angle_velocity
        if pressed_key[pygame.K_LEFT]:
            self.angle -= self.angle_velocity

        if pressed_key[pygame.K_q]:
            self.height += self.velocity
        if pressed_key[pygame.K_e]:
            self.height -= self.velocity

        if pressed_key[pygame.K_w]:
            self.pos[0] += self.velocity * cos_a
            self.pos[1] += self.velocity * sin_a
        if pressed_key[pygame.K_a]:
            self.pos[0] += self.velocity * cos_a
            self.pos[1] -= self.velocity * sin_a
        if pressed_key[pygame.K_s]:
            self.pos[0] -= self.velocity * cos_a
            self.pos[1] -= self.velocity * sin_a
        if pressed_key[pygame.K_d]:
            self.pos[0] -= self.velocity * cos_a
            self.pos[1] += self.velocity * sin_a