import pygame
from src.settings import WHITE, RED, GREEN


class EnemyHealthBar:
    """
    Wyświetla pasek zdrowia nad wrogiem.
    """

    def __init__(self, bar_width=40, bar_height=5, offset_y=-15):
        """
        Inicjalizuje EnemyHealthBar.

        Args:
            bar_width: Szerokość paska (domyślnie 40)
            bar_height: Wysokość paska (domyślnie 5)
            offset_y: Offset Y od górnej krawędzi wroga (domyślnie -15)
        """
        self.bar_width = bar_width
        self.bar_height = bar_height
        self.offset_y = offset_y
        self.color_bg = (50, 50, 50)
        self.color_bar = GREEN
        self.color_border = WHITE

    def draw(self, screen, enemy):
        """
        Rysuje pasek zdrowia wroga.

        Args:
            screen: Powierzchnia pygame do rysowania
            enemy: Obiekt wroga
        """
        if enemy.health <= 0:
            return

        # Oblicz pozycję paska (nad wrogiem)
        bar_x = enemy.rect.centerx - self.bar_width // 2
        bar_y = enemy.rect.top + self.offset_y

        # Tło paska
        bg_rect = pygame.Rect(bar_x, bar_y, self.bar_width, self.bar_height)
        pygame.draw.rect(screen, self.color_bg, bg_rect)
        pygame.draw.rect(screen, self.color_border, bg_rect, 1)

        # Pasek zdrowia
        if enemy.max_health > 0:
            health_progress = enemy.health / enemy.max_health
            health_bar_width = int(self.bar_width * health_progress)
            
            # Zmień kolor w zależności od zdrowia
            if health_progress > 0.5:
                color = GREEN
            elif health_progress > 0.25:
                color = (255, 165, 0)  # Orange
            else:
                color = RED

            health_rect = pygame.Rect(bar_x, bar_y, health_bar_width, self.bar_height)
            pygame.draw.rect(screen, color, health_rect)


class EnemyHealthBarManager:
    """
    Zarządza paskami zdrowia dla wszystkich wrogów.
    """

    def __init__(self):
        """Inicjalizuje EnemyHealthBarManager."""
        self.health_bar = EnemyHealthBar()

    def draw_all(self, screen, enemies):
        """
        Rysuje paski zdrowia dla wszystkich wrogów.

        Args:
            screen: Powierzchnia pygame do rysowania
            enemies: Lista wrogów
        """
        for enemy in enemies:
            self.health_bar.draw(screen, enemy)

