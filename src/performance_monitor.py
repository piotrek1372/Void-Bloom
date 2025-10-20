import pygame
from src.settings import WHITE, BLACK


class PerformanceMonitor:
    """
    Monitoruje wydajność gry.
    Wyświetla FPS, liczbę wrogów, pocisków i innych statystyk.
    """

    def __init__(self, show_debug=False):
        """
        Inicjalizuje PerformanceMonitor.

        Args:
            show_debug: Czy wyświetlać debug info (domyślnie False)
        """
        self.show_debug = show_debug
        self.font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        self.fps = 0
        self.frame_count = 0
        self.frame_time = 0.0
        self.update_interval = 0.5  # Aktualizuj FPS co 0.5 sekundy

    def update(self, dt):
        """
        Aktualizuje monitor wydajności.

        Args:
            dt: Delta czasu od ostatniej klatki
        """
        self.frame_count += 1
        self.frame_time += dt

        if self.frame_time >= self.update_interval:
            self.fps = int(self.frame_count / self.frame_time)
            self.frame_count = 0
            self.frame_time = 0.0

    def draw(self, screen, enemy_count=0, projectile_count=0, gem_count=0):
        """
        Rysuje informacje o wydajności na ekranie.

        Args:
            screen: Powierzchnia pygame do rysowania
            enemy_count: Liczba wrogów
            projectile_count: Liczba pocisków
            gem_count: Liczba klejnotów XP
        """
        if not self.show_debug:
            return

        # Pozycja w prawym górnym rogu
        x = screen.get_width() - 250
        y = 20

        # FPS
        fps_text = self.font.render(f"FPS: {self.fps}", True, WHITE)
        screen.blit(fps_text, (x, y))
        y += 30

        # Liczba wrogów
        enemies_text = self.font.render(f"Wrogowie: {enemy_count}", True, WHITE)
        screen.blit(enemies_text, (x, y))
        y += 30

        # Liczba pocisków
        projectiles_text = self.font.render(f"Pociski: {projectile_count}", True, WHITE)
        screen.blit(projectiles_text, (x, y))
        y += 30

        # Liczba klejnotów
        gems_text = self.font.render(f"Klejnoty: {gem_count}", True, WHITE)
        screen.blit(gems_text, (x, y))

    def toggle_debug(self):
        """Przełącza wyświetlanie debug info."""
        self.show_debug = not self.show_debug

