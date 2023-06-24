import pygame
from PIL import Image
import math
from HelperLibrary import LightingGenerator
from settings import *
import numpy as np

class GrassPlane(pygame.sprite.Sprite):

        
    def update(self,dt):
        
        
        if not self.image or UPDATE:
            self.nextTime(dt)
            self.imageNormals = LightingGenerator.updateWaterNormals(self.imageNormals,self.t*10,[self.x,self.y],self.boat)
            self.image = LightingGenerator.getLitty(self.imageNormals, self.imageColors, (self.width, self.height),LightingGenerator.getLightingVecXZ(self.t))
            
    def nextTime(self,dt):
        self.t+=dt

            
            
    def __init__(self,width, height, pos_x, pos_y, pos_z, scale,boat):
        super().__init__()
        self.imageColors= Image.open(f"src\\Entities\\Grass\\grassColor.png")
        imageNormal = Image.open(f"src\\Entities\\Grass\\grassNormals.png")
        self.imageNormals = np.array(imageNormal.getdata()).reshape(imageNormal.size[0], imageNormal.size[1], 4)
        self.t = 0
        self.z = pos_z
        self.boat = boat
        
        self.scale=scale
        
        
        self.t = math.pi*12
        self.x = pos_x
        self.y = pos_y
        self.image = False
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.update(0)
        