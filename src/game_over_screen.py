import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, BLUE


class GameOverScreen:
    """
    Ekran wyświetlany na koniec demo.
    Pokazuje statystyki gracza i zachęcę do dodania gry do listy życzeń.
    """

    def __init__(self, player_level, total_xp, enemies_killed, time_survived):
        """
        Inicjalizuje GameOverScreen.

        Args:
            player_level: Osiągnięty poziom gracza
            total_xp: Całkowite zebrane XP
            enemies_killed: Liczba zabitych wrogów
            time_survived: Czas przetrwania w sekundach
        """
        self.player_level = player_level
        self.total_xp = total_xp
        self.enemies_killed = enemies_killed
        self.time_survived = time_survived
        self.is_active = True

        # Czcionki
        self.font_title = pygame.font.Font(None, 72)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)

        # Przyciski
        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        """Tworzy przyciski na ekranie."""
        button_width = 300
        button_height = 60
        button_y = SCREEN_HEIGHT - 150

        # Przycisk "Dodaj do listy życzeń Steam"
        wishlist_button = {
            'rect': pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                button_y,
                button_width,
                button_height
            ),
            'text': 'Dodaj do listy życzeń Steam',
            'action': 'wishlist',
            'hovered': False
        }
        self.buttons.append(wishlist_button)

        # Przycisk "Wyjdź"
        exit_button = {
            'rect': pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                button_y + 80,
                button_width,
                button_height
            ),
            'text': 'Wyjdź',
            'action': 'exit',
            'hovered': False
        }
        self.buttons.append(exit_button)

    def handle_mouse_motion(self, pos):
        """
        Obsługuje ruch myszy.

        Args:
            pos: Pozycja myszy (x, y)
        """
        for button in self.buttons:
            button['hovered'] = button['rect'].collidepoint(pos)

    def handle_mouse_click(self, pos):
        """
        Obsługuje klik myszy.

        Args:
            pos: Pozycja kliknięcia (x, y)

        Returns:
            Akcja do wykonania ('wishlist', 'exit', lub None)
        """
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                return button['action']
        return None

    def draw(self, screen):
        """
        Rysuje ekran gry skończonej.

        Args:
            screen: Powierzchnia pygame do rysowania
        """
        # Tło
        screen.fill(BLACK)

        # Tytuł
        title_text = self.font_title.render("DEMO SKOŃCZONE!", True, (255, 215, 0))
        title_rect = title_text.get_rect()
        title_rect.centerx = SCREEN_WIDTH // 2
        title_rect.top = 40
        screen.blit(title_text, title_rect)

        # Statystyki
        stats_y = 150
        stats = [
            f"Osiągnięty Poziom: {self.player_level}",
            f"Całkowite XP: {self.total_xp}",
            f"Zabici Wrogowie: {self.enemies_killed}",
            f"Czas Przetrwania: {int(self.time_survived // 60)}:{int(self.time_survived % 60):02d}"
        ]

        for stat in stats:
            stat_text = self.font_medium.render(stat, True, WHITE)
            stat_rect = stat_text.get_rect()
            stat_rect.centerx = SCREEN_WIDTH // 2
            stat_rect.top = stats_y
            screen.blit(stat_text, stat_rect)
            stats_y += 60

        # Wiadomość
        message_y = stats_y + 40
        message_text = self.font_small.render(
            "Dziękujemy za grę w demo!",
            True,
            (200, 200, 200)
        )
        message_rect = message_text.get_rect()
        message_rect.centerx = SCREEN_WIDTH // 2
        message_rect.top = message_y
        screen.blit(message_text, message_rect)

        # Rysuj przyciski
        for button in self.buttons:
            # Tło przycisku
            color = (100, 150, 255) if button['hovered'] else (50, 100, 200)
            pygame.draw.rect(screen, color, button['rect'])
            pygame.draw.rect(screen, WHITE, button['rect'], 2)

            # Tekst przycisku
            button_text = self.font_small.render(button['text'], True, WHITE)
            button_text_rect = button_text.get_rect()
            button_text_rect.center = button['rect'].center
            screen.blit(button_text, button_text_rect)

    def get_time_string(self):
        """
        Zwraca sformatowany string czasu.

        Returns:
            String w formacie "MM:SS"
        """
        minutes = int(self.time_survived) // 60
        seconds = int(self.time_survived) % 60
        return f"{minutes:02d}:{seconds:02d}"

