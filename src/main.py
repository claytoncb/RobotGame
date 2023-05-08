from PIL import Image
import numpy as np
import math
from numpy.linalg import norm

def getLitty(imageColor, lightingVec, imageNormal, sewerMode):
    colors = np.array(imageColor.getdata()).reshape(imageColor.size[0], imageColor.size[1], 4)

    normals = np.array(imageNormal.getdata()).reshape(imageNormal.size[0], imageNormal.size[1], 4)

    lightContribution = []

    
    for normalRows in normals:
        row = []
        for normal in normalRows:
            normalVec = np.array([(normal[0]-127),(normal[1]-127),(normal[2]-127)])
            if sewerMode: lightingVec[1] = -lightingVec[1]
            lightingVec = lightingVec / norm(lightingVec)
            normalVec = normalVec / norm(normalVec)
            if not (normalVec == 0).all():          
                out = np.dot(normalVec,lightingVec)/(norm(normalVec)*norm(lightingVec))
            else:
                out = 0
            row.append(out)
        lightContribution.append(row)
    bodyMaterial = { i: color for i,color in enumerate(colors[0][:6])}
    bodyColor = bodyMaterial[0]
    faceMaterial = { i: color for i,color in enumerate(colors[1][:4])}
    faceColor = faceMaterial[0]
    eyesMaterial = { i: color for i,color in enumerate(colors[2][:4])}
    eyesColor = eyesMaterial[0]
    newColors = np.zeros((imageColor.size[0], imageColor.size[1],4), dtype=np.uint8)
    for row, colorRow in enumerate(colors):
        for col, color in enumerate(colorRow):
            if (col>5 and not (color==0).all()):
                if (color == bodyColor).all():
                    material = bodyMaterial
                if (color == faceColor).all():
                    material = faceMaterial
                if (color == eyesColor).all():
                    material = eyesMaterial
                index = math.floor(lightContribution[row][col]*(len(material)/2)+(len(material)/2))
                color = material[index]
            newColors[row][col] = color
        

    imageLitty = Image.fromarray(np.array(newColors),'RGBA')
    return imageLitty
def getLightingVecXZ(z):
    return np.array([(math.cos(z/18)),(math.cos(z/18-math.pi/4)),(math.sin(z/18))])
def makeGif(imageColor, imageNormal):
    gif = []
    for z in range(314):
        gif.append(getLitty(imageColor,getLightingVecXZ(z),imageNormal,False))
    gif[0].save('temp_result.gif', save_all=True,optimize=False, append_images=gif[1:], loop=0)

imageColor = Image.open('src\\Textures\\RobotBoy\\robotBoyColor.png')
imageNormal = Image.open('src\\Textures\\RobotBoy\\robotBoyNormals.png')
makeGif(imageColor,imageNormal)
#getLitty(imageColor,np.array([-1,0,1]),imageNormal,false).show()

            