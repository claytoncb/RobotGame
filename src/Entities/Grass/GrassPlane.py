import pygame
from PIL import Image
import math
from HelperLibrary import LightingGenerator
from HelperLibrary import DirectionVector
from settings import *
import numpy as np

class GrassPlane(pygame.sprite.Sprite):
    def calculateContibutions(self):
        self.lightContributions = LightingGenerator.lightContributionFromNormals(self.imageNormals ,LightingGenerator.getLightingVecXZ(self.t))
        

        
    def update(self,dt):
        
        
        if not self.image or UPDATE:
            self.nextTime(dt)
            self.calculateContibutions()
            image = LightingGenerator.getLittyGrass(self.imageColors,self.lightContributions).resize((self.scale,self.scale), resample=Image.Resampling.NEAREST )
            self.image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
            
    def nextTime(self,dt):
        self.t+=dt

            
            
    def __init__(self,width, height, pos_x, pos_y, scale):
        super().__init__()
        self.imageColors= Image.open(f"src\\Entities\\Grass\\grassColor.png")
        imageNormal = Image.open(f"src\\Entities\\Grass\\grassNormals.png")
        self.imageNormals = LightingGenerator.normalsFromNormals(np.array(imageNormal.getdata()).reshape(imageNormal.size[0], imageNormal.size[1], 4))
        self.t = 0
        self.z = 0
        
        self.calculateContibutions()
        
        self.scale=scale
        
        
        self.t = math.pi*12
        self.x = pos_x
        self.y = pos_y
        self.image = False
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.update(0)
        