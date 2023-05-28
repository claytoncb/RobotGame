from PIL import Image
import numpy as np
import math
from numpy.linalg import norm
import pygame
from settings import *



def getLitty(normals, colors, size,lightingVec):
    #mask of visible colors
    mask = (np.array(colors)[:,:,3] >= 150)
    mask2 = (np.array(colors)[:,:,3] <= 80)
    #add dimension to mask for all colors
    expanded_mask = np.repeat(mask[:, :, np.newaxis], 4, axis=2)
    
    #apply mask to normals and subtract 127
    newNormals = np.subtract(np.ma.masked_where(expanded_mask,np.array(normals))[:,:,:3],127)

    #mask colors and remove alpha channel
    colors_rgb = np.array(colors)[:, :, :3].astype(np.uint8)
    colors_rgb[mask2] = 0

    # Compute the dot product between newNormals and lightingVec
    dot_product = np.dot(newNormals, lightingVec)

    # Normalize the dot product
    norm_dot_product = dot_product / (np.array([norm(normal) for normal in newNormals]) * norm(lightingVec))
    
    #pos and neg masks
    posMask = norm_dot_product >= 0
    negMask = norm_dot_product < 0

    # Apply the lighting calculation to positive
    norm_dot_product = 2**(norm_dot_product)
    color_adjust_dot = np.zeros((size[0],size[1],4))
    #shift negative toward purple
    color_adjust_dot[:,:,0][negMask]+=norm_dot_product[negMask]*DARK_COLOR[0]
    color_adjust_dot[:,:,1][negMask]+=norm_dot_product[negMask]*DARK_COLOR[1]
    color_adjust_dot[:,:,2][negMask]+=norm_dot_product[negMask]*DARK_COLOR[2]
    
    color_adjust_dot[:,:,0][posMask]=norm_dot_product[posMask]*colors_rgb[:,:,0][posMask]
    color_adjust_dot[:,:,1][posMask]=norm_dot_product[posMask]*colors_rgb[:,:,1][posMask]
    color_adjust_dot[:,:,2][posMask]=norm_dot_product[posMask]*colors_rgb[:,:,2][posMask]

    #make sure ratio stays the same
    color_adjust_dot[:,:,0]= color_adjust_dot[:,:,0]*(colors_rgb[:,:,0]/(colors_rgb[:,:,0]+colors_rgb[:,:,1]+colors_rgb[:,:,2]))
    color_adjust_dot[:,:,1]= color_adjust_dot[:,:,1]*(colors_rgb[:,:,1]/(colors_rgb[:,:,0]+colors_rgb[:,:,1]+colors_rgb[:,:,2]))
    color_adjust_dot[:,:,2]= color_adjust_dot[:,:,2]*(colors_rgb[:,:,2]/(colors_rgb[:,:,0]+colors_rgb[:,:,1]+colors_rgb[:,:,2]))

    

    #add in alphas
    color_adjust_dot[:,:,3][mask]=255

    newColors = (color_adjust_dot).astype(np.uint8)
    
    return pygame.image.fromstring(bytes(np.array(newColors, dtype=np.uint8).reshape(((size[0]*size[1]))*4)), size, 'RGBA')

def getLightingVecXZ(z):
    return np.array([max(math.cos(z/(18*DAYLIGHT_DIVISOR)),0),min(math.cos(z/(18*DAYLIGHT_DIVISOR)-math.pi/4),0),max(math.sin(z/(18*DAYLIGHT_DIVISOR)),0)])
