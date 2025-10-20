import pygame
pygame.init()
(SCREEN_WIDTH, SCREEN_HEIGHT) = pygame.display.get_desktop_sizes()[0]
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
FPS = 60
BLACK = (0, 0, 0)
GREEN = (0, 250, 0)
RED = (250, 0, 0)
BLUE = (0, 0, 250)
WHITE = (250, 250, 250)