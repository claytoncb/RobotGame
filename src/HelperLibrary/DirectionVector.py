import numpy as np
import pygame
from numpy.linalg import norm
def GetDirectionVector(px,py):
    x,y = pygame.mouse.get_pos()
    direction = np.array([((x-px-32)),((y-py-32))])
    normDirection = direction/norm(direction)
    scaledNormDirection = [normDirection[0],normDirection[1]]
    return scaledNormDirection, norm(direction) if pygame.mouse.get_pressed()[0] else 0