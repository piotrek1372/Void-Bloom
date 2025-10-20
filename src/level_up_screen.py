import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, BLUE
from src.upgrade import UpgradeType
from src.passive_upgrades import PassiveUpgradeType


class LevelUpScreen:
    """
    Wyświetla ekran awansu z 3 opcjami ulepszeń do wyboru.
    Gracz może wybrać ulepszenie klikając na niego.
    """

    def __init__(self, upgrades, level):
        """
        Inicjalizuje LevelUpScreen.

        Args:
            upgrades: Lista 3 ulepszeń do wyświetlenia
            level: Nowy poziom gracza
        """
        self.upgrades = upgrades
        self.level = level
        self.selected_upgrade = None
        self.is_active = True

        # Ustawienia UI
        self.font_title = pygame.font.Font(None, 72)
        self.font_level = pygame.font.Font(None, 48)
        self.font_upgrade = pygame.font.Font(None, 36)
        self.font_description = pygame.font.Font(None, 24)

        # Kolory
        self.color_bg = (20, 20, 40)  # Ciemny niebieski
        self.color_overlay = (0, 0, 0, 180)  # Przezroczysty czarny
        self.color_button = (40, 60, 120)  # Niebieski przycisk
        self.color_button_hover = (60, 100, 180)  # Jaśniejszy niebieski
        self.color_text = WHITE
        self.color_highlight = (255, 215, 0)  # Złoty

        # Oblicz pozycje przycisków
        self.button_width = 300
        self.button_height = 150
        self.button_spacing = 50
        self.total_width = 3 * self.button_width + 2 * self.button_spacing
        self.start_x = (SCREEN_WIDTH - self.total_width) // 2
        self.start_y = SCREEN_HEIGHT // 2 + 50

        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        """Tworzy prostokąty przycisków dla każdego ulepszenia."""
        self.buttons = []
        for i, upgrade in enumerate(self.upgrades):
            x = self.start_x + i * (self.button_width + self.button_spacing)
            y = self.start_y
            rect = pygame.Rect(x, y, self.button_width, self.button_height)
            self.buttons.append({
                'rect': rect,
                'upgrade': upgrade,
                'hovered': False
            })

    def handle_mouse_click(self, pos):
        """
        Obsługuje klik myszy na przycisk ulepszenia.

        Args:
            pos: Pozycja kliknięcia (x, y)

        Returns:
            Wybrane ulepszenie lub None
        """
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                self.selected_upgrade = button['upgrade']
                self.is_active = False
                return button['upgrade']
        return None

    def handle_mouse_motion(self, pos):
        """
        Obsługuje ruch myszy dla efektu hover.

        Args:
            pos: Pozycja myszy (x, y)
        """
        for button in self.buttons:
            button['hovered'] = button['rect'].collidepoint(pos)

    def draw(self, surface):
        """
        Rysuje ekran awansu.

        Args:
            surface: Powierzchnia pygame do rysowania
        """
        # Rysuj półprzezroczysty overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(self.color_bg)
        surface.blit(overlay, (0, 0))

        # Rysuj tytuł "LEVEL UP"
        title_text = self.font_title.render("LEVEL UP!", True, self.color_highlight)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        surface.blit(title_text, title_rect)

        # Rysuj numer poziomu
        level_text = self.font_level.render(f"Poziom {self.level}", True, self.color_text)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        surface.blit(level_text, level_rect)

        # Rysuj instrukcję
        instruction_text = self.font_description.render(
            "Wybierz ulepszenie:",
            True,
            self.color_text
        )
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        surface.blit(instruction_text, instruction_rect)

        # Rysuj przyciski ulepszeń
        for button in self.buttons:
            self._draw_button(surface, button)

    def _draw_button(self, surface, button):
        """
        Rysuje pojedynczy przycisk ulepszenia.

        Args:
            surface: Powierzchnia pygame do rysowania
            button: Słownik z danymi przycisku
        """
        rect = button['rect']
        upgrade = button['upgrade']
        hovered = button['hovered']

        # Wybierz kolor przycisku
        button_color = self.color_button_hover if hovered else self.color_button
        border_color = self.color_highlight if hovered else self.color_text

        # Rysuj przycisk
        pygame.draw.rect(surface, button_color, rect)
        pygame.draw.rect(surface, border_color, rect, 3)

        # Rysuj tekst ulepszenia
        name_text = self.font_upgrade.render(upgrade.name, True, self.color_highlight)
        name_rect = name_text.get_rect(center=(rect.centerx, rect.centery - 30))
        surface.blit(name_text, name_rect)

        # Rysuj opis ulepszenia
        desc_text = self.font_description.render(upgrade.description, True, self.color_text)
        desc_rect = desc_text.get_rect(center=(rect.centerx, rect.centery + 20))
        surface.blit(desc_text, desc_rect)

    def is_finished(self):
        """Sprawdza, czy gracz wybrał ulepszenie."""
        return not self.is_active

    def get_selected_upgrade(self):
        """Zwraca wybrane ulepszenie."""
        return self.selected_upgrade

