import pygame
from PIL import Image
import math
from HelperLibrary import LightingGenerator
from settings import *
import numpy as np

class RobotBoy(pygame.sprite.Sprite):
    def calculateContibutions(self):
        self.lightContributionsRight = LightingGenerator.lightContributionFromNormals(self.imageNormalsRight[self.z%len(self.keyframes)] ,LightingGenerator.getLightingVecXZ(self.t))
        self.lightContributionsLeft = LightingGenerator.lightContributionFromNormals(self.imageNormalsLeft[self.z%len(self.keyframes)] ,LightingGenerator.getLightingVecXZ(self.t)) 
    def update(self,dt):
        
        self.nextTime(dt)
        self.calculateContibutions()
        self.input(dt)

        
        if not self.image or UPDATE:
            
            image = LightingGenerator.getLitty(self.imageColors[self.z%len(self.keyframes)],LightingGenerator.getLightingVecXZ(self.t),self.lightContributions).resize((self.scale,self.scale), resample=Image.Resampling.NEAREST )
            self.image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
    def nextAnimation(self,dt):
        self.z+=1
    def nextTime(self,dt):
        self.t+=dt
    def input (self,dt):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            if BUTTON_FEEDBACK: print('left')  
            self.imageColors = self.imageColorsLeft
            self.lightContributions = self.lightContributionsLeft
        if keys[K_RIGHT]:
            if BUTTON_FEEDBACK: print('right') 
            self.imageColors = self.imageColorsRight
            self.lightContributions = self.lightContributionsRight
        if keys[K_UP]:
            if BUTTON_FEEDBACK: print('up')  
        if keys[K_DOWN]:
            if BUTTON_FEEDBACK: print('down')
        if keys[K_LEFT] or keys[K_RIGHT] or keys[K_UP] or keys[K_DOWN]:
            self.nextAnimation(dt)
        else:
            self.z = 0

            
            
    def __init__(self,width, height, pos_x, pos_y, scale):
        super().__init__()
        self.keyframes = [0,1,2,1,0,3,4,3]
        #self.keyframes = [0,2,0,4]
        self.imageColorsLeft = [ Image.open(f"src\\Entities\\RobotBoy\\Textures\\robotBoyColor{i}.png") for i in self.keyframes ]
        self.imageNormalsLeft = [np.array(imageNormal.getdata()).reshape(imageNormal.size[0], imageNormal.size[1], 4) for imageNormal in[ Image.open(f"src\\Entities\\RobotBoy\\Textures\\robotBoyNormals{i}.png") for i in self.keyframes ]]
        self.imageColorsRight = [ Image.open(f"src\\Entities\\RobotBoy\\Textures\\robotBoyColorRight{i}.png") for i in self.keyframes ]
        self.imageNormalsRight = [np.array(imageNormal.getdata()).reshape(imageNormal.size[0], imageNormal.size[1], 4) for imageNormal in[ Image.open(f"src\\Entities\\RobotBoy\\Textures\\robotBoyNormalsRight{i}.png") for i in self.keyframes ]]
        self.t = 0
        self.z = 1
        
        self.calculateContibutions()
        self.lightContributions = self.lightContributionsLeft
        self.imageColors = self.imageColorsLeft
        self.imageNormals= self.imageNormalsLeft
        
        self.scale=scale
        
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False
        self.t = math.pi*12
        self.x = pos_x
        self.y = pos_y
        self.image = False
        self.update(0)
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(self.x, self.y, width, height)