import pygame
class GrassChunk(pygame.sprite.Sprite):
    def __init__(self,image,x,y,width,height):
        super().__init__()
        self.image = image
        self.x = x
        self.y = y
        self.height = height
        self.width=width
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
