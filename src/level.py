from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from Entities.Grass.GrassPlane import GrassPlane
from Entities.RobotBoy.Body import Body
from Entities.RobotBoy.Head import Head
from settings import *

class Level:
    def __init__(self):

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite groups
        self.all_sprites = CameraGroup()
        self.robot = pygame.sprite.Group()
        self.body = Body(64,64,SCREEN_WIDTH/2-32,SCREEN_HEIGHT/2-32,SCALE)
        self.head = Head(64,64,SCREEN_WIDTH/2-32,SCREEN_HEIGHT/2-32,SCALE)
        self.robot.add(self.body)
        self.robot.add(self.head)
        self.plane = GrassPlane(64,64,SCREEN_WIDTH/2+18,SCREEN_HEIGHT/2-28,SCALE)
        #for plane in [GrassPlane(64,64,SCREEN_WIDTH/2+18*i,SCREEN_HEIGHT/2-28*i,SCALE) for i in range(5)]+[GrassPlane(64,64,SCREEN_WIDTH/2-18*(i+1),SCREEN_HEIGHT/2+28*(i+1),SCALE) for i in range(5)]:
        #self.all_sprites.add(self.plane)
        self.all_sprites.add(self.robot)
        

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