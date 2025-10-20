import pygame
import os
import math


class XPGem:
    """
    Reprezentuje klejnot doświadczenia (XP) upuszczany przez wrogów.
    Klejnot może być zbierany przez gracza, a także przyciągany przez magnes XP.
    """

    def __init__(self, x, y, xp_value=10, image_path=None):
        """
        Inicjalizuje XPGem.

        Args:
            x: Początkowa pozycja X
            y: Początkowa pozycja Y
            xp_value: Ilość XP, którą daje klejnot (domyślnie 10)
            image_path: Ścieżka do pliku obrazu (domyślnie crystal.png)
        """
        if image_path is None:
            image_path = os.path.join('assets', 'gfx', 'crystal.png')

        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Statystyki klejnotu
        self.xp_value = xp_value
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_speed = 300  # Maksymalna prędkość przyciągania

    def move(self, dt):
        """
        Przesuwa klejnot na podstawie prędkości.

        Args:
            dt: Delta czasu od ostatniej klatki
        """
        self.rect.centerx += self.velocity_x * dt
        self.rect.centery += self.velocity_y * dt

    def attract_to_player(self, player_x, player_y, dt, magnet_distance=150, magnet_strength=500):
        """
        Przyciąga klejnot w kierunku gracza, jeśli jest w zasięgu magnesu.

        Args:
            player_x: Pozycja X gracza
            player_y: Pozycja Y gracza
            dt: Delta czasu od ostatniej klatki
            magnet_distance: Dystans, w którym magnes zaczyna działać (piksele)
            magnet_strength: Siła przyciągania (przyspieszenie)
        """
        # Oblicz dystans do gracza
        dx = player_x - self.rect.centerx
        dy = player_y - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        # Jeśli klejnot jest w zasięgu magnesu, przyciągnij go
        if distance < magnet_distance and distance > 0:
            # Znormalizuj kierunek
            dx_norm = dx / distance
            dy_norm = dy / distance

            # Zastosuj przyspieszenie w kierunku gracza
            self.velocity_x += dx_norm * magnet_strength * dt
            self.velocity_y += dy_norm * magnet_strength * dt

            # Ograniczaj prędkość do maksymalnej
            speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
            if speed > self.max_speed:
                self.velocity_x = (self.velocity_x / speed) * self.max_speed
                self.velocity_y = (self.velocity_y / speed) * self.max_speed

    def update(self, dt, player_x, player_y):
        """
        Aktualizuje stan klejnotu (przyciąganie, ruch).

        Args:
            dt: Delta czasu od ostatniej klatki
            player_x: Pozycja X gracza
            player_y: Pozycja Y gracza
        """
        self.attract_to_player(player_x, player_y, dt)
        self.move(dt)

    def draw(self, surface):
        """
        Rysuje klejnot na powierzchni.

        Args:
            surface: Powierzchnia pygame do rysowania
        """
        surface.blit(self.image, self.rect.topleft)

    def is_collected(self, player_rect, collection_distance=50):
        """
        Sprawdza, czy klejnot został zebrany przez gracza.

        Args:
            player_rect: Rect gracza
            collection_distance: Dystans, w którym klejnot jest zbierany (piksele)

        Returns:
            True jeśli klejnot został zebrany, False w przeciwnym razie
        """
        distance = math.sqrt(
            (self.rect.centerx - player_rect.centerx)**2 +
            (self.rect.centery - player_rect.centery)**2
        )
        return distance < collection_distance

    def is_off_screen(self, screen_width, screen_height, margin=100):
        """
        Sprawdza, czy klejnot wyszedł poza ekran.

        Args:
            screen_width: Szerokość ekranu
            screen_height: Wysokość ekranu
            margin: Margines poza ekranem (piksele)

        Returns:
            True jeśli klejnot jest poza ekranem, False w przeciwnym razie
        """
        return (self.rect.right < -margin or self.rect.left > screen_width + margin or
                self.rect.bottom < -margin or self.rect.top > screen_height + margin)

