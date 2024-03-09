import pygame
from setting import Direction
class Bullet:
    def __init__(self,x,y,direction,image='./images/bullet/0.png'):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.speed = 50
    def move(self):
        if self.direction == Direction.LEFT:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
    def draw(self,screen):
        screen.blit(self.image,self.rect)