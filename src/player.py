import pygame, os
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self):
        self.image = pygame.image.load(os.path.join('assets', 'gfx', 'player.png'))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.velocity_x = 0
        self.velocity_y = 0
        self.acc = 45
        self.max_velocity_y = 50
        self.max_velocity_x = 120
        self.rect = self.image.get_rect()
        self.rect.topleft = (SCREEN_WIDTH // 20, SCREEN_HEIGHT // 2 - self.rect.height)
        self.cooldown_timer = 0
        self.cooldown_duration = 0.5
        self.reloaded = True
    def input(self, keys, dt):
        if keys[pygame.K_d]:
            self.velocity_x += self.acc * dt
        elif keys[pygame.K_a]:
            self.velocity_x -= self.acc * dt
        else:
            if self.velocity_x > 0:
                self.velocity_x -= self.acc * dt
                if self.velocity_x < 1:
                    self.velocity_x = 0
            elif self.velocity_x < 0:
                self.velocity_x += self.acc * dt
                if self.velocity_x > -1:
                    self.velocity_x = 0
        if keys[pygame.K_w]:
            self.velocity_y -= self.acc * dt
        elif keys[pygame.K_s]:
            self.velocity_y += self.acc * dt
        else:
            if self.velocity_y > 0:
                self.velocity_y -= self.acc * dt
                if self.velocity_y < 1:
                    self.velocity_y = 0
            elif self.velocity_y < 0:
                self.velocity_y += self.acc * dt
                if self.velocity_y > -1:
                    self.velocity_y = 0

    def physics(self):
        if self.rect.left < SCREEN_WIDTH // 20:
            self.rect.left = SCREEN_WIDTH // 20
            self.velocity_x = 0
        elif self.rect.right > SCREEN_WIDTH // 2:
            self.rect.right = SCREEN_WIDTH // 2
            self.velocity_x = 0
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.velocity_y > self.max_velocity_y:
            self.velocity_y = self.max_velocity_y
        elif self.velocity_y < self.max_velocity_y * -1:
            self.velocity_y = self.max_velocity_y * -1
        if self.velocity_x > self.max_velocity_x:
            self.velocity_x = self.max_velocity_x
        elif self.velocity_x < self.max_velocity_x * -1:
            self.velocity_x = self.max_velocity_x * -1
    def move(self, dt):
        self.rect.left += self.velocity_x * dt
        self.rect.top += self.velocity_y * dt
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def reload(self, dt):
        self.reloaded = False
        if self.reloaded == False:
            self.cooldown_timer += dt
            if self.cooldown_timer >= self.cooldown_duration:
                self.cooldown_timer = 0
                self.reloaded = True