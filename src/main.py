from PIL import Image
import numpy as np
import math
from numpy.linalg import norm

def lightContributionFromNormals(normals, lightingVec):
    lightContribution = []
    for normalRows in normals:
        row = []
        for normal in normalRows:
            normalVec = np.array([(normal[0]-127),(normal[1]-127),(normal[2]-127)])
            lightingVec = lightingVec / norm(lightingVec)
            normalVec = normalVec / norm(normalVec)
            if not (normalVec == 0).all():          
                out = np.dot(normalVec,lightingVec)/(norm(normalVec)*norm(lightingVec))
            else:
                out = 0
            row.append(out)
        lightContribution.append(row)
    return lightContribution

def getLitty(imageColor, lightingVec, imageNormal):
    colors = np.array(imageColor.getdata()).reshape(imageColor.size[0], imageColor.size[1], 4)
    normals = np.array(imageNormal.getdata()).reshape(imageNormal.size[0], imageNormal.size[1], 4)
    lightContribution = lightContributionFromNormals(normals,lightingVec)

    
    
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
                elif (color == faceColor).all():
                    material = faceMaterial
                elif (color == eyesColor).all():
                    material = eyesMaterial
                else:
                    newColors[row][col] = [0,0,0,0]
                    break
                index = math.floor(lightContribution[row][col]*(len(material)/2)+(len(material)/2))
                color = material[index]
                newColors[row][col] = color
            else:
                newColors[row][col] = [0,0,0,0]
        

    imageLitty = Image.fromarray(np.array(newColors),'RGBA')
    return imageLitty
def getLightingVecXZ(z):
    return np.array([(math.cos(z/18)),(math.cos(z/18-math.pi/4)),(math.sin(z/18))])

def makeGif(imageColors, imageNormals,keyframes):
    gif = []
    for z in range(314):
        gif.append(getLitty(imageColors[z%len(keyframes)],getLightingVecXZ(z),imageNormals[z%len(keyframes)]).resize((512,512), resample=Image.Resampling.NEAREST ))
    gif[0].save('temp_result.gif', save_all=True,optimize=False, append_images=gif[1:], loop=0)

def reverse_rows_and_save(filenames):
    for i,img in enumerate(filenames):

        # Reverse the rows of the image
        rgb = Image.Image.split(img)

        # Swap the red and blue channels
        img = Image.merge("RGBA", (rgb[2], rgb[1], rgb[0],rgb[3]))

        
        arr = np.array(img)

# Slice the array to remove the first 6 pixels in the first 3 rows
        old = np.array(arr[0:3, 0:6, :])
        arr[0:3, 0:6, :] = 0

# Convert the NumPy array back to an image
        img = Image.fromarray(arr)


        # Reverse the rows of the cropped image
        img = img.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)

        arr = np.array(img)

# Slice the array to remove the first 6 pixels in the first 3 rows
        print(f"old values: {old}")
        arr[0:3, 0:6, :] = old
        print(f"new values: {arr[0:3, 0:6, :]}")
        #arr = np.roll(arr,-1,axis=1)
        img = Image.fromarray(arr)
        

        # Paste the flipped image back into the original image

        # Create the new filename
        new_filename = f"src\\Entities\\Ship\\Textures\\Ship{i+100}N.png"

        # Save the reversed image to the new filename
        img.save(new_filename)

#keyframes = [0,1,2,1,0,3,4,3]
#keyframes = [1,2,3,4,5]
imageColors = [ Image.open(f"src\\Entities\\Ship\\Textures\\Ship{i}N.png") for i in keyframes ]
#imageNormals = [ Image.open(f"src\\Textures\\RobotBoy\\robotBoyNormals{i}.png") for i in keyframes ]
#makeGif(imageColors,imageNormals,keyframes)
reverse_rows_and_save(imageColors)
#getLitty(imageColor,np.array([-1,0,1]),imageNormal).show()

            