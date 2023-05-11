import pygame
from PIL import Image
import math
from HelperLibrary import LightingGenerator
from HelperLibrary import DirectionVector
from Entities.Grass.GrassChunk.GrassChunk import GrassChunk
from settings import *
import numpy as np

class GrassPlane(pygame.sprite.Group):
    def calculateContibutions(self):
        self.lightContributions = LightingGenerator.lightContributionFromNormals(self.imageNormals ,LightingGenerator.getLightingVecXZ(self.t))
        image = LightingGenerator.getLittyGrass(self.imageColors,self.lightContributions).resize((self.scale,self.scale), resample=Image.Resampling.NEAREST )
        self.image =  pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        

        
    def update(self,dt):
        if UPDATE:
            self.nextTime(dt)
            self.calculateContibutions()
            for chunk in self.chunks:
                chunk.image = self.image
            
            
    def nextTime(self,dt):
        self.t+=dt

            
            
    def __init__(self,width, height, pos_x, pos_y, scale):
        super().__init__()
        self.imageColors= Image.open(f"src\\Entities\\Grass\\grassColor.png")
        imageNormal = Image.open(f"src\\Entities\\Grass\\grassNormals.png")
        self.imageNormals = np.array(imageNormal.getdata()).reshape(imageNormal.size[0], imageNormal.size[1], 4)
        self.t = 0
        self.z = 0
        self.t = math.pi*12
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = height
        
        
        
        self.scale=scale
        self.calculateContibutions()
        self.chunks = [GrassChunk(self.image,i*20,i*20,self.width,self.height) for i in range(10)]
        for chunk in self.chunks:
            self.add(chunk)
        
        
        self.update(0)
        