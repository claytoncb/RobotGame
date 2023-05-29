from PIL import Image
import numpy as np
import math
from numpy.linalg import norm
import pygame
from settings import *



def getLitty(normals, colors, size,lightingVec):
    lightingVec = lightingVec/norm(lightingVec)
    #mask of visible colors
    maskVisible = (np.array(normals)[:,:,3] > 100)
    maskNotVisible = (np.array(normals)[:,:,3] == 0)
    

    #add dimension to mask for all colors
    expanded_mask = np.repeat(maskVisible[:, :, np.newaxis], 4, axis=2)
    
    #apply mask to normals and subtract 127
    newNormals = np.subtract(np.ma.masked_where(expanded_mask,np.array(normals))[:,:,:3],127)

    #mask colors and remove alpha channel
    colors_rgb = np.array(colors)[:, :, :3].astype(np.uint8)
    colors_rgb[maskNotVisible] = 0

    # Compute the dot product between newNormals and lightingVec (SIGMOID)
    norm_dot_product = 1/(1+np.exp(-np.dot(newNormals/128, lightingVec)*SUN_BRIGHTNESS))


    # Apply the lighting calculation to positive
    color_adjust_dot = np.zeros((size[0],size[1],4))
    brightness = ((colors_rgb[:,:,0]+colors_rgb[:,:,1]+colors_rgb[:,:,2])/(255*3))
    notSource = (brightness < SOURCE_CUTOFF )
    source = (brightness >= SOURCE_CUTOFF )

    color_adjust_dot[:,:,0][notSource]=(DARK_COLOR[0]+brightness[notSource]*(colors_rgb[:,:,0][notSource]))+norm_dot_product[notSource]*(colors_rgb[:,:,0][notSource]-(DARK_COLOR[0]+brightness[notSource]*(colors_rgb[:,:,0][notSource])))
    color_adjust_dot[:,:,1][notSource]=(DARK_COLOR[1]+brightness[notSource]*(colors_rgb[:,:,0][notSource]))+norm_dot_product[notSource]*(colors_rgb[:,:,1][notSource]-(DARK_COLOR[1]+brightness[notSource]*(colors_rgb[:,:,1][notSource])))
    color_adjust_dot[:,:,2][notSource]=(DARK_COLOR[2]+brightness[notSource]*(colors_rgb[:,:,0][notSource]))+norm_dot_product[notSource]*(colors_rgb[:,:,2][notSource]-(DARK_COLOR[2]+brightness[notSource]*(colors_rgb[:,:,2][notSource])))
    color_adjust_dot[:,:,0][source]=(colors_rgb[:,:,0][source])
    color_adjust_dot[:,:,1][source]=(colors_rgb[:,:,1][source])
    color_adjust_dot[:,:,2][source]=(colors_rgb[:,:,2][source])

    

    #shift negative toward purple as a function of brightness (aka sum of rgb of colors)
    


    

    #add in alphas
    color_adjust_dot[:,:,3][maskVisible]=255

    newColors = (color_adjust_dot).astype(np.uint8)
    
    return pygame.image.fromstring(bytes(np.array(newColors, dtype=np.uint8).reshape(((size[0]*size[1]))*4)), size, 'RGBA')

def getLightingVecXZ(z):
    return np.array([math.cos(z/(18*DAYLIGHT_DIVISOR)-math.pi*4/9),2*min(math.sin(z/(18*DAYLIGHT_DIVISOR)-math.pi/4),0),math.sin(z/(18*DAYLIGHT_DIVISOR)-math.pi*4/9)])
