import pygame, os
from src.settings import SCREEN, FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from src.player import Player
from src.bullet import Bullet

pygame.init()
SCREEN

def load_background():
    try:
        background_path = os.path.join('assets', 'gfx', 'parallax-space-background.png')
        return background_path
    except pygame.error as e:
        print(f"Nie można załadować obrazka tła: {background_path}")
        print(e)

def scale_background():
    path = load_background()
    image = pygame.image.load(path).convert()
    image_width = image.get_width()
    image_height = image.get_height()
    scaled_w = SCREEN_WIDTH / image_width
    scaled_h = SCREEN_HEIGHT / image_height
    scale = max(scaled_w, scaled_h)
    image_width *= scale
    image_height *= scale
    return pygame.transform.scale(image, (int(image_width), int(image_height)))
def main():
    clock = pygame.time.Clock()
    run = True
    player = Player()
    bullets = []
    scaled_background = scale_background()
    while run:
        dt = clock.tick(FPS) / 1000
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
        SCREEN.blit(scaled_background, (0, 0))
        player.input(keys, dt)
        player.physics()
        player.move(dt)
        player.draw(SCREEN)
        player.reload(dt)
        if keys[pygame.K_SPACE] and player.reloaded == True:
                bullet = Bullet(player.rect.right, player.rect.centery)
                bullets.append(bullet)
        for bullet in bullets.copy():
            bullet.draw(SCREEN)
            bullet.move(dt)
            if bullet.rect.left >= SCREEN_WIDTH:
                bullets.remove(bullet)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()