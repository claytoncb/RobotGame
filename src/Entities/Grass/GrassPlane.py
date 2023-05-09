import pygame
from PIL import Image
import math
from HelperLibrary import LightingGenerator

class GrassPlane(pygame.sprite.Sprite):
    def next(self):
        image = LightingGenerator.getLittyGrass(self.imageColors,LightingGenerator.getLightingVecXZ(self.t),self.imageNormals).resize((self.scale,self.scale), resample=Image.Resampling.NEAREST )
        self.image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
    def nextAnimation(self):
        self.z+=1
    def nextTime(self):
        self.t+=1
    def __init__(self,width, height, pos_x, pos_y, pos_z):
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
        self.scale = 128
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = height
        self.next()
        self.rect = pygame.rect.Rect(self.x, self.y, width, height)