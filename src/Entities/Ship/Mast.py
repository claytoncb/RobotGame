import pygame
from PIL import Image
import math
from HelperLibrary import LightingGenerator
from settings import *
import numpy as np
from HelperLibrary import DirectionVector

class Mast(pygame.sprite.Sprite):        
    def update(self,dt):
        
        self.nextTime(dt)
        
        
        dvec,mag = DirectionVector.GetDirectionVector(self.x,self.y)
        self.speed = JOYSTICK_CONTRIBUTION*dvec*mag+(1-JOYSTICK_CONTRIBUTION)*self.speed
        self.input()
        self.x_prev = self.x
        self.y_prev = self.y
        self.rect = pygame.rect.Rect(self.x+self.offsets[self.z%len(self.directions)][0]+WAVE_SHIP_MOVEMENT[0]*np.sin(self.t*WAVE_SHIP_MOVEMENT_FREQ[0]), self.y+self.offsets[self.z%len(self.directions)][1]+WAVE_SHIP_MOVEMENT[1]*np.cos(self.t*WAVE_SHIP_MOVEMENT_FREQ[1]), self.width, self.height)

        
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
        self.offsets = [(0,-14),(-1,-9),(2,-10),(3,-6),(4,-7),(2,-3),(0,-6),(-2,-3),(-4,-7),(-3,-7),(-2,-10),(0,-9)]
        self.imageColors= [ Image.open(f"src\\Entities\\Ship\\Textures\\Mast{i}C.png") for i in self.directions ]
        self.imageNormals = [np.array(imageNormal.getdata()).reshape(imageNormal.size[0], imageNormal.size[1], 4) for imageNormal in[ Image.open(f"src\\Entities\\Ship\\Textures\\Mast{i}N.png") for i in self.directions ]]
        self.t = 0
        self.z = pos_z

        self.movingLeft = True
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False
        
        
        self.scale=scale
        
        
        self.t = math.pi*12
        self.width = width
        self.height = height
        self.x = pos_x + self.width*3/7
        self.y = pos_y + self.height*5/7
        self.image = False
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.update(0)
        