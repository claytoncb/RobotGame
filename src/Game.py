import pygame, sys

from Entities.RobotBoy import RobotBoy
from Entities.Grass import GrassPlane

    
pygame.init()
clock = pygame.time.Clock()

screen_width = screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height), flags=pygame.SCALED, vsync=1)

robotGuy = RobotBoy(64,64,screen_width/2-50,screen_height/2-50,0)
grassPlanes = [GrassPlane(64,64,screen_width/2+36*i,screen_height/2-56*i,0) for i in range(5)]

group = pygame.sprite.Group()
for grassPlane in grassPlanes:
    group.add(grassPlane)
group.add(robotGuy)
grassPlane = grassPlanes[0]

main = True
while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            main = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                grassPlane.movingLeft = True
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                grassPlane.movingRight = True
            if event.key == pygame.K_UP or event.key == ord('w'):
                grassPlane.movingUp = True
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                grassPlane.movingDown= True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                grassPlane.movingLeft = False
                robotGuy.z = 0
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                grassPlane.movingRight = False
                robotGuy.z = 0
            if event.key == pygame.K_UP or event.key == ord('w'):
                grassPlane.movingUp = False
                robotGuy.z = 0
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                grassPlane.movingDown = False
                robotGuy.z = 0
            if event.key == ord('q'):
                pygame.quit()
                main = False
                sys.exit()
        
        if grassPlane.movingLeft ^ grassPlane.movingRight:
            for object in group:
                object.nextAnimation()
                if grassPlane.movingLeft:
                    if not isinstance(object, RobotBoy):
                        object.x+=16
                    robotGuy.imageColors = robotGuy.imageColorsLeft
                    robotGuy.imageNormals= robotGuy.imageNormalsLeft
                elif grassPlane.movingRight:
                    if not isinstance(object, RobotBoy):
                        object.x-=16
                    robotGuy.imageColors = robotGuy.imageColorsRight
                    robotGuy.imageNormals= robotGuy.imageNormalsRight
                if grassPlane.movingDown:
                    if not isinstance(object, RobotBoy):
                        object.y-=8
                elif grassPlane.movingUp:
                    if not isinstance(object, RobotBoy):
                        object.y+=8
                if (grassPlane.movingRight or grassPlane.movingLeft) or (grassPlane.movingUp or grassPlane.movingDown):
                    if not isinstance(object, RobotBoy):
                        object.rect = pygame.rect.Rect(object.x, object.y, object.width, object.height)
        screen.fill([0,0,0,0])
        for object in group:
            object.next()
            object.nextTime()
        group.draw(screen)
        pygame.display.update()
        clock.tick(60)