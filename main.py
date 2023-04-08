import pygame
from player import Player
from renderer import Renderer
from settings import *

class App:
    def __init__(self):
        self.res = self.width, self.height = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.res, pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.renderer = Renderer(self)
        self.running = True

    def update(self):
        self.player.update()
        self.renderer.update()
    
    def draw(self):
        self.renderer.draw()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.update()
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.clock.tick(FPS)
            pygame.display.set_caption(f"FPS : {self.clock.get_fps():.2f}")

if __name__ == "__main__":
    pygame.init()
    app = App()
    app.run()
    pygame.quit()