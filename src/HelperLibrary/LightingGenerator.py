from PIL import Image
import numpy as np
import math
from numpy.linalg import norm
import pygame
from settings import *

def magnitude(vector):
    return np.sqrt(np.sum(np.power(vector,2),axis=1))

def updateWaterNormals(normals,t,offset,boat, islands):
    boat_x = boat.x + boat.width*3/7
    boat_y = boat.y + boat.height*5/7
    boat_x_prev = boat.x_prev + boat.width*3/7
    boat_y_prev = boat.y_prev + boat.height*5/7
    t=t*WAVE_TIME_SCALE
    t2 = np.sin(t)
    t3 = -.2*t-t2
    x = np.arange(0, 128)
    y = np.arange(0, 128)
    xx, yy = np.meshgrid(x, y)
        
    circle_xx = xx+offset[0]-boat_x
    circle_yy = yy+offset[1]-boat_y
    dist = np.sqrt(np.square(circle_xx)+np.square(2*(circle_yy)))
    result_x2 = WAKE_AMPLITUDE*np.exp(-np.square(WAKE_RADIUSISH*dist))*(np.sin(WAKE_FREQ*math.pi/64*dist+t)+np.sin(WAKE_FREQ*math.pi/32*dist+t)+np.sin(WAKE_FREQ*math.pi/16*dist+t)+np.sin(WAKE_FREQ*math.pi/8*dist+t))/2
    
    circle_xx_prev = xx+offset[0]-boat_x_prev
    circle_yy_prev = yy+offset[1]-boat_y_prev
    dist_prev = np.sqrt(np.square(circle_xx_prev)+np.square(2*(circle_yy_prev)))
    result_x2_prev = WAKE_AMPLITUDE*np.exp(-np.square(.85*WAKE_RADIUSISH*dist_prev))*(np.sin(WAKE_FREQ*math.pi/64*dist_prev+t)+np.sin(WAKE_FREQ*math.pi/32*dist_prev+t)+np.sin(WAKE_FREQ*math.pi/16*dist_prev+t)+np.sin(WAKE_FREQ*math.pi/8*dist_prev+t))/2
    result_x3=0
    for island in islands:
        circle_xx = xx+offset[0]-island.x-16
        circle_yy = yy+offset[1]-island.y-16
        dist = np.sqrt(np.square(circle_xx)+np.square(2*(circle_yy)))
        result_x3 += WAKE_AMPLITUDE*2*np.exp(-np.square(WAKE_RADIUSISH*dist))*(np.sin(WAKE_FREQ*math.pi/64*dist+t3)+np.sin(WAKE_FREQ*math.pi/32*dist+t3)+np.sin(WAKE_FREQ*math.pi/16*dist+t3)+np.sin(WAKE_FREQ*math.pi/8*dist+t3))/2

    xx -= math.floor(boat.speed[0])
    yy -= math.floor(boat.speed[1])

    result_x = (2*WAVE_AMPLITUDE*np.sin(((xx+t2*WAVE_SPEED+offset[0])+(yy+t2*WAVE_SPEED+offset[1])*2)*math.pi/32)+2*WAVE_AMPLITUDE*np.sin(((-xx+t2*WAVE_SPEED+offset[0])+(yy+t2*WAVE_SPEED+offset[1])*2)*math.pi/64+t)+WAVE_AMPLITUDE*np.sin(((-xx+t2*WAVE_SPEED)+(yy+t2*WAVE_SPEED+offset[1])*1.1)*math.pi/16+t)+WAVE_AMPLITUDE*np.sin(((xx+t2*WAVE_SPEED+offset[0])+(yy+t2*WAVE_SPEED+offset[1])*4)*math.pi/24+t))/6
    result_z = (2*WAVE_AMPLITUDE*np.cos(((xx+t2*WAVE_SPEED+offset[0])+(yy+t2*WAVE_SPEED+offset[1])*2)*math.pi/32)+2*WAVE_AMPLITUDE*np.cos(((-xx+t2*WAVE_SPEED+offset[0])+(yy+t2*WAVE_SPEED+offset[1])*2)*math.pi/64+t)+WAVE_AMPLITUDE*np.cos(((-xx+t2*WAVE_SPEED)+(yy+t2*WAVE_SPEED+offset[1])*1.1)*math.pi/16+t)+WAVE_AMPLITUDE*np.cos(((xx+t2*WAVE_SPEED+offset[0])+(yy+t2*WAVE_SPEED+offset[1])*4)*math.pi/24+t))/6
    
    result_x = (result_x + result_x2+result_x3 + result_x2_prev)
    result_z = (result_z + result_x2+result_x3 + result_x2_prev)

    combined_wave = np.ones((128,128,4))*255
    combined_wave[:,:,0] = result_x
    combined_wave[:,:,1] = 240
    combined_wave[:,:,2] = result_z
    combined_wave = combined_wave
    normals=np.array(combined_wave,dtype=np.int32)
    return normals

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
    norm_dot_product = ((np.dot(newNormals, lightingVec)+1)/2).reshape((size[0]*size[1]))/128
    
    

    #apply sigmoid
    #norm_dot_product = 1/(1+np.exp(-norm_dot_product))
    


    # Apply the lighting calculation to positive
    full_norms = np.zeros((size[0]*size[1],3))
    full_norms[:,0] = norm_dot_product
    full_norms[:,1] = norm_dot_product
    full_norms[:,2] = norm_dot_product

    #Camera angle and light reflection off normal calculations for highlights
    reflection_angles = (-(full_norms*(newNormals/128))*2)+np.tile(lightingVec,(size[0]*size[1],1))
    bounce_light = np.zeros((size[0]*size[1],3))
    bounce_light[:,0] = (np.dot(-reflection_angles,np.array(CAMERA_ANGLE/norm(CAMERA_ANGLE))) + 1) /2
    bounce_light[:,1] = bounce_light[:,0]
    bounce_light[:,2] = bounce_light[:,0]
    norm_dot_product = (norm_dot_product + 1) /2
    full_norms[:,0] = norm_dot_product
    full_norms[:,1] = norm_dot_product
    full_norms[:,2] = norm_dot_product

    highlights = (bounce_light[:,0] > .60)
    bounce_light[highlights] = bounce_light[highlights] - 0.60

    color_adjust_dot = np.zeros((size[0]*size[1],3))

    #adding darkness when sun angle is low
    color_adjust_dot=((DARK_COLOR)-full_norms*((DARK_COLOR)-(colors_rgb*.7+LIGHT_COLOR*.3)))

    #adding highlights when bounce light is similar to camera angle
    #color_adjust_dot[highlights] = color_adjust_dot[highlights]*(1-bounce_light[highlights]) + LIGHT_COLOR*(bounce_light[highlights])
    color_adjust_dot[highlights] = LIGHT_COLOR*bounce_light[highlights]+(1-bounce_light[highlights])*color_adjust_dot[highlights]
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
    y=max(3*math.sin(z/(18*DAYLIGHT_DIVISOR)-math.pi*12/4),-2.5)
    x=math.sin(z/(18*DAYLIGHT_DIVISOR)-math.pi*3/4)
    z=-math.sin(z/(18*DAYLIGHT_DIVISOR)-math.pi/4)
    return np.array([x*y+(1-y)*x,y,z*y+(1-y)*z])
    #return np.array([-math.sin(z/(18*DAYLIGHT_DIVISOR)),2*min(math.sin((z-(7.5*math.pi/2))/(18*DAYLIGHT_DIVISOR)-math.pi/4),0),math.cos(z/(18*DAYLIGHT_DIVISOR))])
