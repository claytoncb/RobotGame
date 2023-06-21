import pygame
from PIL import Image
import math
from HelperLibrary import LightingGenerator
from settings import *
import numpy as np
from HelperLibrary import DirectionVector

class Ship(pygame.sprite.Sprite):        
    def update(self,dt):
        
        self.nextTime(dt)
        
        
        dvec,mag = DirectionVector.GetDirectionVector(self.x,self.y)
        self.speed = JOYSTICK_CONTRIBUTION*dvec*mag+(1-JOYSTICK_CONTRIBUTION)*self.speed
        self.input()
        self.x+=self.speed[0]+WIND_VECTOR[0]
        self.y+=self.speed[1]+WIND_VECTOR[1]
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

        
        if not self.image or UPDATE:
            self.image = LightingGenerator.getLitty(self.imageNormals[self.z%len(self.directions)], self.imageColors[self.z%len(self.directions)], (self.width, self.height),LightingGenerator.getLightingVecXZ(self.t))
            
    def nextTime(self,dt):
        self.t+=dt
        
    def input (self):
        x,y = pygame.mouse.get_pos()
        self.z = (math.floor(math.atan2(self.speed[1],self.speed[0])/math.pi*6+6.5)-3)%12

            
            
    def __init__(self,width, height, pos_x, pos_y, pos_z, scale):
        super().__init__()
        self.speed=0
        self.directions = [12,1,2,3,4,5,6,7,8,9,10,11]
        self.imageColors= [ Image.open(f"src\\Entities\\Ship\\Textures\\Ship{i}C.png") for i in self.directions ]
        self.imageNormals = [np.array(imageNormal.getdata()).reshape(imageNormal.size[0], imageNormal.size[1], 4) for imageNormal in[ Image.open(f"src\\Entities\\Ship\\Textures\\Ship{i}N.png") for i in self.directions ]]
        self.t = 0
        self.z = pos_z

        self.movingLeft = True
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False
        
        
        self.scale=scale
        
        
        self.t = math.pi*12
        self.x = pos_x
        self.y = pos_y
        self.image = False
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.update(0)
        