from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from Entities.Grass.GrassPlane import GrassPlane
from Entities.RobotBoy.Body import Body
from Entities.RobotBoy.Head import Head
from Entities.Ship.Ship import Ship
from Entities.Ship.Mast import Mast
from Entities.Island0.Island0 import Island0
from settings import *

class Level:
    def __init__(self):

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite groups
        self.all_sprites = CameraGroup()
        self.vessel = pygame.sprite.Group()
        self.islands = pygame.sprite.Group()
        self.body = Body(64,64,SCREEN_WIDTH/2-32,SCREEN_HEIGHT/2-32, 0, SCALE)
        self.head = Head(64,64,SCREEN_WIDTH/2-32,SCREEN_HEIGHT/2-32, 32, SCALE)
        self.ship = Ship(32,32,SCREEN_WIDTH/2-32,SCREEN_HEIGHT/2-32, 32, SCALE)
        self.mast = Mast(32,32,SCREEN_WIDTH/2-32,SCREEN_HEIGHT/2-32, 32, SCALE)

        #adding island
        self.island = Island0(32,32,SCREEN_WIDTH/2-32,SCREEN_HEIGHT/2-32, 32, SCALE,self.ship)
        self.islands.add(self.island)

        #adding water
        for j in range(4):
            for i in range(4):
                plane = GrassPlane(128, 128, 128*i, 128*j, 0, SCALE,self.ship, self.islands) 
                self.all_sprites.add(plane)
        self.all_sprites.add(self.islands)
        

        #adding ship
        self.vessel.add(self.ship)
        self.vessel.add(self.mast)
        self.all_sprites.add(self.vessel)
        

    def run(self,dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw()
        self.all_sprites.update(dt)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image,sprite.rect)