import pygame
from PIL import Image
import math
from HelperLibrary import LightingGenerator
from HelperLibrary import DirectionVector
from settings import *
import numpy as np

class Body(pygame.sprite.Sprite):
    def calculateContibutions(self):
        self.lightContributions = LightingGenerator.lightContributionFromNormals(self.imageNormals ,LightingGenerator.getLightingVecXZ(self.t))
        

        
    def update(self,dt):
        
        self.nextTime(dt)
        dvec,mag = DirectionVector.GetDirectionVector(self.x,self.y)
        if mag > WANDER_DIST:
            self.x+=dvec[0]*SPEED
            self.y+=dvec[1]*SPEED
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

        

        
        if not self.image or UPDATE:
            self.calculateContibutions()
            self.image = LightingGenerator.getLitty(self.imageColors,self.lightContributions)
            
    def nextTime(self,dt):
        self.t+=dt

            
            
    def __init__(self,width, height, pos_x, pos_y, scale):
        super().__init__()
        self.directions = [12,1,2,3,4,5,6,7,8,9,10,11]
        #self.keyframes = [0,2,0,4]
        self.imageColors= Image.open(f"src\\Entities\\RobotBoy\\Textures\\body\\BodyC.png")
        imageNormal = Image.open(f"src\\Entities\\RobotBoy\\Textures\\body\\Body.png")
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
        