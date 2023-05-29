import pygame
from PIL import Image
import math
from HelperLibrary import LightingGenerator
from HelperLibrary import DirectionVector
from settings import *
import numpy as np

class Body(pygame.sprite.Sprite):
        
    def update(self,dt):
        
        self.nextTime(dt)
        dvec,mag = DirectionVector.GetDirectionVector(self.x,self.y)
        self.speed = .2*dvec*mag+.8*self.speed
        self.x+=self.speed[0]
        self.y+=self.speed[1]
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

        

        
        if not self.image or UPDATE:
            self.image = LightingGenerator.getLitty(self.imageNormals, self.imageColors, (self.width, self.height),LightingGenerator.getLightingVecXZ(self.t))
            
    def nextTime(self,dt):
        self.t+=dt

            
            
    def __init__(self,width, height, pos_x, pos_y, pos_z, scale):
        super().__init__()
        self.speed=0
        self.imageColors= Image.open(f"src\\Entities\\RobotBoy\\Textures\\body\\BodyC.png")
        imageNormal = Image.open(f"src\\Entities\\RobotBoy\\Textures\\body\\Body.png")
        self.imageNormals = np.array(imageNormal.getdata()).reshape(imageNormal.size[0], imageNormal.size[1], 4)
        self.t = 0
        self.z = pos_z
        
        self.scale=scale
        
        
        self.t = math.pi*12
        self.x = pos_x
        self.y = pos_y
        self.image = False
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.update(0)
        