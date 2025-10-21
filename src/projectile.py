import pygame
import os
from abc import ABC, abstractmethod


class Projectile(ABC):
    """
    Bazowa klasa dla wszystkich pocisków w grze.
    Zawiera wspólne właściwości i metody dla zarządzania pociskami.
    """

    def __init__(self, x, y, image_path, speed=350, damage=10, lifetime=None, direction_x=1, direction_y=0, weapon_source=None, piercing=False):
        """
        Inicjalizuje Projectile.

        Args:
            x: Początkowa pozycja X
            y: Początkowa pozycja Y
            image_path: Ścieżka do pliku obrazu
            speed: Prędkość pocisku (piksele na sekundę)
            damage: Obrażenia zadawane przez pocisk
            lifetime: Czas życia pocisku w sekundach (None = nieskończony)
            direction_x: Kierunek na osi X (-1, 0, 1)
            direction_y: Kierunek na osi Y (-1, 0, 1)
            weapon_source: Referencja do broni, która wystrzelił ten pocisk
            piercing: Czy pocisk przechodzi przez wrogów (True/False lub liczba przebić)
        """
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Statystyki pocisku
        self.speed = speed
        self.damage = damage
        self.lifetime = lifetime
        self.elapsed_time = 0.0

        # Kierunek ruchu (znormalizowany wektor)
        self.direction_x = direction_x
        self.direction_y = direction_y

        # Referencja do broni, która wystrzelił ten pocisk
        self.weapon_source = weapon_source

        # Atrybut piercing - określa czy pocisk przechodzi przez wrogów
        # True = przechodzi przez wszystkich wrogów (nieskończone przebicia)
        # False = usuwany po trafieniu (0 przebić)
        # liczba > 0 = liczba przebić zanim pocisk zostanie usunięty
        self.piercing = piercing
        self.piercing_count = 0  # Licznik przebić (dla liczb > 0)

    def move(self, dt):
        """
        Przesuwa pocisk na podstawie prędkości i kierunku.

        Args:
            dt: Delta czasu od ostatniej klatki
        """
        displacement = self.speed * dt
        self.rect.left += self.direction_x * displacement
        self.rect.top += self.direction_y * displacement

    def update(self, dt):
        """
        Aktualizuje stan pocisku (ruch, czas życia).

        Args:
            dt: Delta czasu od ostatniej klatki

        Returns:
            True jeśli pocisk powinien być usunięty, False w przeciwnym razie
        """
        self.move(dt)

        # Aktualizuj czas życia
        if self.lifetime is not None:
            self.elapsed_time += dt
            if self.elapsed_time >= self.lifetime:
                return True  # Pocisk powinien być usunięty

        return False  # Pocisk powinien pozostać

    def draw(self, surface):
        """
        Rysuje pocisk na powierzchni.

        Args:
            surface: Powierzchnia pygame do rysowania
        """
        surface.blit(self.image, self.rect.topleft)

    def is_off_screen(self, screen_width, screen_height):
        """
        Sprawdza, czy pocisk wyszedł poza ekran.

        Args:
            screen_width: Szerokość ekranu
            screen_height: Wysokość ekranu

        Returns:
            True jeśli pocisk jest poza ekranem, False w przeciwnym razie
        """
        return (
            self.rect.right < 0
            or self.rect.left > screen_width
            or self.rect.bottom < 0
            or self.rect.top > screen_height
        )


class Bullet(Projectile):
    """
    Konkretna implementacja pocisku - zwykła kula.
    Dziedziczy z Projectile i ustawia domyślne parametry dla zwykłej kuli.
    """

    def __init__(self, x, y, speed=350, damage=10, weapon_source=None):
        """
        Inicjalizuje Bullet.

        Args:
            x: Początkowa pozycja X
            y: Początkowa pozycja Y
            speed: Prędkość pocisku (domyślnie 350)
            damage: Obrażenia (domyślnie 10)
            weapon_source: Referencja do broni, która wystrzelił ten pocisk
        """
        image_path = os.path.join('assets', 'gfx', 'bullet.png')
        super().__init__(
            x=x,
            y=y - 32,  # Przesunięcie w górę
            image_path=image_path,
            speed=speed,
            damage=damage,
            lifetime=None,  # Kula żyje nieskończenie długo
            direction_x=1,  # Porusza się w prawo
            direction_y=0,
            weapon_source=weapon_source,
            piercing=False  # Zwykłe kule są usuwane po trafieniu
        )

