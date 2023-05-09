import pygame, sys

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
                    newColors[row][col] = [1,1,1,1]
                    break
                index = math.floor(lightContribution[row][col]*(len(material)/2)+(len(material)/2))
                color = material[index]
                newColors[row][col] = color
            else:
                newColors[row][col] = [1,1,1,1]
        

    imageLitty = Image.fromarray(np.array(newColors),'RGBA')
    return imageLitty

def getLightingVecXZ(z):
    return np.array([(math.cos(z/18)),(math.cos(z/18-math.pi/4)),(math.sin(z/18))])

class RobotGuy(pygame.sprite.Sprite):
    def next(self):
        image = getLitty(self.imageColors[self.z%len(self.keyframes)],getLightingVecXZ(self.t),self.imageNormals[self.z%len(self.keyframes)]).resize((self.scale,self.scale), resample=Image.Resampling.NEAREST )
        self.image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
    def nextAnimation(self):
        self.z+=1
    def nextTime(self):
        self.t+=.01
    def __init__(self,width, height, pos_x, pos_y, pos_z):
        super().__init__()
        self.keyframes = [0,1,2,1,0,3,4,3]
        self.imageColorsLeft = [ Image.open(f"src\\Textures\\RobotBoy\\robotBoyColor{i}.png") for i in self.keyframes ]
        self.imageNormalsLeft = [ Image.open(f"src\\Textures\\RobotBoy\\robotBoyNormals{i}.png") for i in self.keyframes ]
        self.imageColorsRight = [ Image.open(f"src\\Textures\\RobotBoy\\robotBoyColorRight{i}.png") for i in self.keyframes ]
        self.imageNormalsRight = [ Image.open(f"src\\Textures\\RobotBoy\\robotBoyNormalsRight{i}.png") for i in self.keyframes ]
        self.imageColors = self.imageColorsLeft
        self.imageNormals= self.imageNormalsLeft
        self.z = 1
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False
        self.t = math.pi*12
        self.scale = 128
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = height
        self.next()
        self.rect = pygame.rect.Rect(self.x, self.y, width, height)

class GrassPlane(pygame.sprite.Sprite):
    def next(self):
        image = getLitty(self.imageColors,getLightingVecXZ(self.t),self.imageNormals).resize((self.scale,self.scale), resample=Image.Resampling.NEAREST )
        self.image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
    def nextAnimation(self):
        self.z+=1
    def nextTime(self):
        self.t+=.01
    def __init__(self,width, height, pos_x, pos_y, pos_z):
        super().__init__()
        self.keyframes = [0,1,2,1,0,3,4,3]
        self.imageColors = Image.open(f"src\\Textures\\RobotBoy\\grassColor.png")
        self.imageNormals= Image.open(f"src\\Textures\\RobotBoy\\grassNormals.png")
        self.z = 1
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False
        self.t = math.pi*12
        self.scale = 128
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = height
        self.next()
        self.rect = pygame.rect.Rect(self.x, self.y, width, height)
    
pygame.init()
clock = pygame.time.Clock()

screen_width = screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height), flags=pygame.SCALED, vsync=1)

robotGuy = RobotGuy(50,50,screen_height/2-50,screen_width/2-50,0)
grassPlane = GrassPlane(50,50,screen_height/2,screen_width/2,0)

group = pygame.sprite.Group()
group.add(grassPlane)
group.add(robotGuy)

main = True
while main:
    for event in pygame.event.get():
        for object in group:
            object.nextTime()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                print('left')
                grassPlane.movingLeft = True
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                print('right')
                grassPlane.movingRight = True
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('up')
                grassPlane.movingUp = True
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                print('down')
                grassPlane.movingDown= True

                

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                print('left stop')
                grassPlane.movingLeft = False
                grassPlane.z = 0
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                print('right stop')
                grassPlane.movingRight = False
                grassPlane.z = 0
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('up stop')
                grassPlane.movingUp = False
                grassPlane.z = 0
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                print('down stop')
                grassPlane.movingDown = False
                grassPlane.z = 0
            if event.key == ord('q'):
                pygame.quit()
                main = False
                sys.exit()
        
        if grassPlane.movingLeft ^ grassPlane.movingRight:
            grassPlane.nextAnimation()
            robotGuy.nextAnimation()
            if grassPlane.movingLeft:
                for object in group:
                    if not isinstance(object, RobotGuy):
                        object.x+=8
                robotGuy.imageColors = robotGuy.imageColorsLeft
                robotGuy.imageNormals= robotGuy.imageNormalsLeft
            elif grassPlane.movingRight:
                grassPlane.x-=8
                robotGuy.imageColors = robotGuy.imageColorsRight
                robotGuy.imageNormals= robotGuy.imageNormalsRight
            if grassPlane.movingDown:
                grassPlane.y-=4
            elif grassPlane.movingUp:
                grassPlane.y+=4
            if (grassPlane.movingRight or grassPlane.movingLeft) or (grassPlane.movingUp or grassPlane.movingDown):
                grassPlane.rect = pygame.rect.Rect(grassPlane.x, grassPlane.y, grassPlane.width, grassPlane.height)
        screen.fill([255,255,255])
        for object in group:
            object.next()
        group.draw(screen)
        pygame.display.update()