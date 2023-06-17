from PIL import Image
import numpy as np
import math
from numpy.linalg import norm
import pygame
from settings import *



def getLitty(normals, colors, size,lightingVec):
    lightingVec = lightingVec/norm(lightingVec)
    #mask of visible colors
    maskVisible = (np.array(normals)[:,:,3].reshape((size[0]*size[1])) > 100)
    maskNotVisible = (np.array(normals)[:,:,3].reshape((size[0]*size[1])) == 0)
    

    #add dimension to mask for all colors
    expanded_mask = np.repeat(maskVisible[ :, np.newaxis], 4, axis=1).reshape((size[0]*size[1],4))
    
    #apply mask to normals and subtract 127
    newNormals = (np.subtract(np.ma.masked_where(expanded_mask,np.array(normals).reshape((size[0]*size[1],4))),127)/128).reshape((size[0]*size[1],4))

    #mask colors and remove alpha channel
    colors_rgb = np.array(colors)[:, :, :3].astype(np.uint8).reshape((size[0]*size[1],3))
    newNormals = newNormals[:,:3]
    

    # Compute the dot product between newNormals and lightingVec
    norm_dot_product = ((np.dot(newNormals.reshape((size[0]*size[1],3)), lightingVec)+1)/2).reshape((size[0]*size[1]))/128

    #apply sigmoid
    #norm_dot_product = 1/(1+np.exp(-norm_dot_product))
    norm_dot_product = (norm_dot_product + 1) /2


    # Apply the lighting calculation to positive
    full_norms = np.zeros((size[0]*size[1],3))
    full_norms[:,0] = norm_dot_product
    full_norms[:,1] = norm_dot_product
    full_norms[:,2] = norm_dot_product

    color_adjust_dot = np.zeros((size[0]*size[1],3))

    color_adjust_dot=(DARK_COLOR)-full_norms*((DARK_COLOR)-(colors_rgb))
    colors_rgb[maskNotVisible] = 0
    color_adjust_dot.reshape((size[0],size[1],3))
    
    dot = np.zeros((size[0],size[1],4))
    dot[:,:,:3] = color_adjust_dot.reshape(size[0],size[1],3)
    dot[:,:,3][maskVisible.reshape((size[0],size[1]))]=255
    color_adjust_dot=dot
    

    #shift negative toward purple as a function of brightness (aka sum of rgb of colors)
    


    

    #add in alphas
    

    newColors = (color_adjust_dot).astype(np.uint8)
    
    return pygame.image.fromstring(bytes(np.array(newColors, dtype=np.uint8).reshape(((size[0]*size[1]))*4)), size, 'RGBA')

def getLightingVecXZ(z):
    return np.array([math.cos(z/(18*DAYLIGHT_DIVISOR)-math.pi*4/9),2*min(math.sin(z/(18*DAYLIGHT_DIVISOR)-math.pi/4),0),math.sin(z/(18*DAYLIGHT_DIVISOR)-math.pi*4/9)])
