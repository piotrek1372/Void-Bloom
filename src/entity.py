import pygame
import os
from abc import ABC, abstractmethod


class Entity(ABC):
    """
    Bazowa klasa dla wszystkich bytów w grze (gracze, wrogowie, itp.).
    Zawiera wspólne właściwości i metody dla zarządzania pozycją, prędkością i rysowaniem.
    """

    def __init__(self, x, y, image_path, max_velocity_x=100, max_velocity_y=100, acceleration=45):
        """
        Inicjalizuje Entity.

        Args:
            x: Początkowa pozycja X
            y: Początkowa pozycja Y
            image_path: Ścieżka do pliku obrazu
            max_velocity_x: Maksymalna prędkość na osi X
            max_velocity_y: Maksymalna prędkość na osi Y
            acceleration: Przyspieszenie
        """
        self.image = pygame.image.load(image_path)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Prędkość i przyspieszenie
        self.velocity_x = 0
        self.velocity_y = 0
        self.acc = acceleration
        self.max_velocity_x = max_velocity_x
        self.max_velocity_y = max_velocity_y

    def move(self, dt):
        """
        Przesuwa Entity na podstawie prędkości.

        Args:
            dt: Delta czasu od ostatniej klatki
        """
        self.rect.left += self.velocity_x * dt
        self.rect.top += self.velocity_y * dt

    def apply_velocity_limits(self):
        """Ogranicza prędkość do maksymalnych wartości."""
        if self.velocity_y > self.max_velocity_y:
            self.velocity_y = self.max_velocity_y
        elif self.velocity_y < -self.max_velocity_y:
            self.velocity_y = -self.max_velocity_y

        if self.velocity_x > self.max_velocity_x:
            self.velocity_x = self.max_velocity_x
        elif self.velocity_x < -self.max_velocity_x:
            self.velocity_x = -self.max_velocity_x

    @abstractmethod
    def physics(self):
        """
        Abstrakcyjna metoda do implementacji fizyki specyficznej dla danego bytu.
        Każda podklasa musi ją zaimplementować.
        """
        pass

    @abstractmethod
    def update(self, dt):
        """
        Abstrakcyjna metoda do aktualizacji stanu bytu.
        Każda podklasa musi ją zaimplementować.

        Args:
            dt: Delta czasu od ostatniej klatki
        """
        pass

    def draw(self, surface):
        """
        Rysuje Entity na powierzchni.

        Args:
            surface: Powierzchnia pygame do rysowania
        """
        surface.blit(self.image, self.rect.topleft)

