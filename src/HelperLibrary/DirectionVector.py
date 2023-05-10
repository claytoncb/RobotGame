import numpy as np
import pygame
from numpy.linalg import norm
def GetDirectionVector():
    x,y = pygame.mouse.get_pos()
    direction = np.array([((y-256)/256),((x-256)/256)])
    normDirection = direction/norm(direction)
    scaledNormDirection = [normDirection[1],normDirection[0]]
    return scaledNormDirection