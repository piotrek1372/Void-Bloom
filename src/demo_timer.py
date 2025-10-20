import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK


class DemoTimer:
    """
    Zarządza czasem trwania demo.
    Wyświetla odliczanie i kończy grę po upływie czasu.
    """

    def __init__(self, duration_seconds=600):
        """
        Inicjalizuje DemoTimer.

        Args:
            duration_seconds: Czas trwania demo w sekundach (domyślnie 600 = 10 minut)
        """
        self.total_duration = duration_seconds
        self.elapsed_time = 0.0
        self.is_active = True
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

    def update(self, dt):
        """
        Aktualizuje timer.

        Args:
            dt: Delta czasu od ostatniej klatki

        Returns:
            True jeśli demo się skończyło, False w przeciwnym razie
        """
        if not self.is_active:
            return False

        self.elapsed_time += dt

        if self.elapsed_time >= self.total_duration:
            self.is_active = False
            return True

        return False

    def get_remaining_time(self):
        """
        Zwraca pozostały czas w sekundach.

        Returns:
            Liczba sekund pozostałych
        """
        remaining = self.total_duration - self.elapsed_time
        return max(0, remaining)

    def get_time_string(self):
        """
        Zwraca sformatowany string czasu.

        Returns:
            String w formacie "MM:SS"
        """
        remaining = self.get_remaining_time()
        minutes = int(remaining) // 60
        seconds = int(remaining) % 60
        return f"{minutes:02d}:{seconds:02d}"

    def draw(self, screen):
        """
        Rysuje timer na ekranie.

        Args:
            screen: Powierzchnia pygame do rysowania
        """
        time_string = self.get_time_string()

        # Rysuj tło dla timera
        timer_text = self.font_large.render(time_string, True, WHITE)
        timer_rect = timer_text.get_rect()
        timer_rect.topright = (SCREEN_WIDTH - 20, 20)

        # Rysuj tło
        bg_rect = timer_rect.inflate(20, 10)
        pygame.draw.rect(screen, BLACK, bg_rect)
        pygame.draw.rect(screen, WHITE, bg_rect, 2)

        # Rysuj tekst
        screen.blit(timer_text, timer_rect)

        # Ostrzeżenie gdy zostało mniej niż 1 minuta
        remaining = self.get_remaining_time()
        if remaining < 60:
            warning_text = self.font_small.render("KONIEC DEMO!", True, (255, 0, 0))
            warning_rect = warning_text.get_rect()
            warning_rect.topright = (SCREEN_WIDTH - 20, 80)
            screen.blit(warning_text, warning_rect)

    def get_progress(self):
        """
        Zwraca postęp demo (0.0 - 1.0).

        Returns:
            Procent czasu, który upłynął
        """
        return min(1.0, self.elapsed_time / self.total_duration)

