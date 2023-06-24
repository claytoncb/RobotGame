import numpy as np
import pygame
from numpy.linalg import norm
from settings import *
def GetDirectionVector(px,py):
    x,y = pygame.mouse.get_pos()
    direction = np.array([((x-px-16)),((y-py-8))])
    normDirection = direction/norm(direction)
    scaledNormDirection = np.array([normDirection[0],normDirection[1]])*ACCELERATION
    mag = norm(direction) if (pygame.mouse.get_pressed()[0] or not PRESS_TO_MOVE) else 0
    return scaledNormDirection, min(mag,MAX_MAG)*SPEED