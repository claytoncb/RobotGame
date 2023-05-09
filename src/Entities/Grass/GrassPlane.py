import pygame
from PIL import Image
import math
from HelperLibrary import LightingGenerator
from settings import *

class GrassPlane(pygame.sprite.Sprite):
    def update(self,dt):
        self.input()
        self.nextTime(dt)
        image = LightingGenerator.getLittyGrass(self.imageColors,LightingGenerator.getLightingVecXZ(self.t),self.imageNormals).resize((self.scale,self.scale), resample=Image.Resampling.NEAREST )
        self.image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
    def nextTime(self,dt):
        self.t+=dt/DAYLIGHT_DIVISOR
    def input (self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            if BUTTON_FEEDBACK: print('left')
            self.x+=5
        if keys[K_RIGHT]:
            if BUTTON_FEEDBACK: print('right')
            self.x-=5
        if keys[K_UP]:
            if BUTTON_FEEDBACK: print('up')
            self.y+=5
        if keys[K_DOWN]:
            if BUTTON_FEEDBACK: print('down')
            self.y-=5
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
    def __init__(self,width, height, pos_x, pos_y, scale):
        super().__init__()
        self.keyframes = [0,1,2,1,0,3,4,3]
        self.imageColors = Image.open(f"src\\Entities\\Grass\\grassColor.png")
        self.imageNormals= Image.open(f"src\\Entities\\Grass\\grassNormals.png")
        self.z = 1
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False
        self.t = math.pi*12
        self.scale = scale
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = height
        self.update(0)