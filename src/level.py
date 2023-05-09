import pygame
from Entities.Grass import GrassPlane
from Entities.RobotBoy import RobotBoy
from settings import *

class Level:
    def __init__(self):

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.robotGuy = RobotBoy.RobotBoy(64,64,SCREEN_WIDTH/2-50,SCREEN_HEIGHT/2-50,SCALE)
        self.grassPlanes = pygame.sprite.Group()
        for plane in [GrassPlane.GrassPlane(64,64,SCREEN_WIDTH/2+18*i,SCREEN_HEIGHT/2-28*i,SCALE) for i in range(5)]+[GrassPlane.GrassPlane(64,64,SCREEN_WIDTH/2-18*(i+1),SCREEN_HEIGHT/2+28*(i+1),SCALE) for i in range(5)]:
            self.grassPlanes.add(plane)
        self.all_sprites.add(self.grassPlanes)
        self.all_sprites.add(self.robotGuy)
        

    def run(self,dt):
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)