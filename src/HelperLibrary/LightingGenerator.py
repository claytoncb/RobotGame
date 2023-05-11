from PIL import Image
import numpy as np
import math
from numpy.linalg import norm

def lightContributionFromNormals(normals, lightingVec):
    lightContribution = []
    for row, normalRows in enumerate(normals):
        for col, normal in enumerate(normalRows):
            if normal[3]>0:
                normalVec = np.array([(normal[0]-127),(normal[1]-127),(normal[2]-127)])
                lightingVec = lightingVec / norm(lightingVec)
                normalVec = normalVec / norm(normalVec)
                out = np.dot(normalVec,lightingVec)/(norm(normalVec)*norm(lightingVec))
                if not np.isnan(out):
                    lightContribution.append(((row,col),out))
    return lightContribution

def getLittyGrass(imageColor, lightContribution):
    colors = np.array(imageColor.getdata()).reshape(imageColor.size[0], imageColor.size[1], 4)

    bodyMaterial = { i: color for i,color in enumerate(colors[0][:8])}
    bodyColor = bodyMaterial[0]
    newColors = np.zeros((imageColor.size[0], imageColor.size[1],4), dtype=np.uint8)
    for x in lightContribution: 
        contribution = x[1]
        row =x[0][0]
        col = x[0][1]
        color = colors[row][col]
        if not (row<=2 and col <= 6):
            if (color == bodyColor).all():
                material = bodyMaterial
                newColors[row][col] = material[math.floor(contribution*(len(material)/2)+(len(material)/2))]
    

    imageLitty = Image.fromarray(np.array(newColors),'RGBA')
    return imageLitty

def getLitty(imageColor, lightContribution):
    colors = np.array(imageColor.getdata()).reshape(imageColor.size[0], imageColor.size[1], 4)

    bodyMaterial = { i: color for i,color in enumerate(colors[0][:6])}
    bodyColor = bodyMaterial[0]
    faceMaterial = { i: color for i,color in enumerate(colors[1][:4])}
    faceColor = faceMaterial[0]
    eyesMaterial = { i: color for i,color in enumerate(colors[2][:4])}
    eyesColor = eyesMaterial[0]

    newColors = np.zeros((imageColor.size[0], imageColor.size[1],4), dtype=np.uint8)

    for x in lightContribution: 
        contribution = x[1]
        row =x[0][0]
        col = x[0][1]
        color = colors[row][col]
        if not (row<=2 and col <= 6):
            if (color == bodyColor).all():
                material = bodyMaterial
                newColors[row][col] = material[math.floor(contribution*(len(material)/2)+(len(material)/2))]
            elif (color == faceColor).all():
                material = faceMaterial
                newColors[row][col] = material[math.floor(contribution*(len(material)/2)+(len(material)/2))]
            elif (color == eyesColor).all():
                material = eyesMaterial
                newColors[row][col] = material[math.floor(contribution*(len(material)/2)+(len(material)/2))]
                
            

    imageLitty = Image.fromarray(np.array(newColors),'RGBA')
    return imageLitty

def getLightingVecXZ(z):
    return np.array([(math.cos(z/18)),(math.cos(z/18-math.pi/4)),(math.sin(z/18))])