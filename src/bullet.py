import pygame, os

class Bullet:
    def __init__(self, x, y):
        self.image = pygame.image.load(os.path.join('assets', 'gfx', 'bullet.png'))
        self.rect = self.image.get_rect()
        self.speed = 350
        self.x = x
        self.y = y - 32
        self.rect.topleft = (self.x, self.y)

    def move(self, dt):
        self.rect.left += self.speed * dt

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)