import pygame, sys
from settings import *
from Entities.Grass.GrassPlane import GrassPlane
from level import Level
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SCALED, vsync=1)
        pygame.display.set_caption("RoboLad")
        self.clock = pygame.time.Clock()
        self.level = Level()
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick()/1000
            self.level.run(dt)
            pygame.display.update()
if __name__ == '__main__':
    game = Game()
    game.run()