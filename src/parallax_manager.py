import pygame
import math
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class ParallaxManager:
    """
    Zarządza efektem parallax scrolling dla tła i wrogów.
    Tworzy iluzję nieskończonego lotu w kosmosie poprzez przesuwanie elementów
    z różnymi prędkościami w zależności od ich "głębokości".
    """

    def __init__(self, background_image_path):
        """
        Inicjalizuje ParallaxManager.

        Args:
            background_image_path: Ścieżka do obrazu tła
        """
        self.background_image = pygame.image.load(background_image_path).convert()
        self.background_width = self.background_image.get_width()
        self.background_height = self.background_image.get_height()
        
        # Pozycja przesunięcia tła (dla efektu parallax)
        self.offset_x = 0
        self.offset_y = 0
        
        # Prędkość przesunięcia gracza (do obliczania parallax)
        self.player_velocity_x = 0
        self.player_velocity_y = 0
        
        # Współczynnik parallax dla różnych warstw
        # 0.0 = statyczne, 1.0 = pełna prędkość gracza
        self.parallax_depth = 0.3  # Tło porusza się wolniej niż gracz

    def update(self, player_velocity_x, player_velocity_y, dt):
        """
        Aktualizuje pozycję parallax na podstawie ruchu gracza.

        Args:
            player_velocity_x: Prędkość gracza na osi X
            player_velocity_y: Prędkość gracza na osi Y
            dt: Delta czasu od ostatniej klatki
        """
        # Przesuwaj tło w kierunku przeciwnym do ruchu gracza
        # Współczynnik parallax_depth sprawia, że tło porusza się wolniej
        self.offset_x += player_velocity_x * self.parallax_depth * dt
        self.offset_y += player_velocity_y * self.parallax_depth * dt
        
        # Zapewniaj, że przesunięcie zawija się (seamless tiling)
        self.offset_x = self.offset_x % self.background_width
        self.offset_y = self.offset_y % self.background_height

    def draw_background(self, screen):
        """
        Rysuje tło z efektem parallax.

        Args:
            screen: Powierzchnia pygame do rysowania
        """
        # Rysuj główne tło
        screen.blit(self.background_image, (-self.offset_x, -self.offset_y))
        
        # Rysuj kopie tła dla seamless wrapping
        # Prawo
        if self.offset_x > 0:
            screen.blit(self.background_image, (self.background_width - self.offset_x, -self.offset_y))
        
        # Dół
        if self.offset_y > 0:
            screen.blit(self.background_image, (-self.offset_x, self.background_height - self.offset_y))
        
        # Prawo-dół
        if self.offset_x > 0 and self.offset_y > 0:
            screen.blit(self.background_image, (self.background_width - self.offset_x, self.background_height - self.offset_y))

    def get_parallax_offset(self, depth=1.0):
        """
        Zwraca przesunięcie parallax dla danej głębokości.
        Używane do przesuwania wrogów i innych elementów.

        Args:
            depth: Współczynnik głębokości (0.0 = statyczne, 1.0 = pełna prędkość)

        Returns:
            Tuple (offset_x, offset_y) dla danej głębokości
        """
        return (self.offset_x * depth, self.offset_y * depth)

    def reset(self):
        """Resetuje parallax do pozycji początkowej."""
        self.offset_x = 0
        self.offset_y = 0

