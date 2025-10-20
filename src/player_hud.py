import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GREEN


class PlayerHUD:
    """
    Wyświetla statystyki gracza na ekranie.
    Pokazuje: poziom, HP, XP, aktywne bronie.
    """

    def __init__(self):
        """Inicjalizuje PlayerHUD."""
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 24)
        
        # Kolory
        self.color_text = WHITE
        self.color_hp_bg = (50, 50, 50)
        self.color_hp_bar = GREEN
        self.color_xp_bg = (50, 50, 50)
        self.color_xp_bar = (100, 150, 255)
        
        # Pozycje
        self.hud_padding = 15
        self.bar_width = 200
        self.bar_height = 20

    def draw(self, screen, player):
        """
        Rysuje HUD gracza na ekranie.

        Args:
            screen: Powierzchnia pygame do rysowania
            player: Obiekt gracza
        """
        # Pozycja lewego górnego rogu HUD
        x = self.hud_padding
        y = self.hud_padding

        # Rysuj poziom
        self._draw_level(screen, player, x, y)
        y += 50

        # Rysuj HP
        self._draw_health(screen, player, x, y)
        y += 60

        # Rysuj XP
        self._draw_xp(screen, player, x, y)
        y += 60

        # Rysuj aktywne bronie
        self._draw_weapons(screen, player, x, y)

    def _draw_level(self, screen, player, x, y):
        """Rysuje informacje o poziomie."""
        level = player.get_level()
        level_text = self.font_large.render(f"Poziom: {level}", True, self.color_text)
        screen.blit(level_text, (x, y))

    def _draw_health(self, screen, player, x, y):
        """Rysuje pasek zdrowia."""
        # Tekst
        health_text = self.font_medium.render(
            f"HP: {int(player.health)}/{int(player.max_health)}",
            True,
            self.color_text
        )
        screen.blit(health_text, (x, y))

        # Pasek zdrowia
        bar_y = y + 30
        self._draw_bar(
            screen,
            x,
            bar_y,
            player.health,
            player.max_health,
            self.color_hp_bar,
            self.color_hp_bg
        )

    def _draw_xp(self, screen, player, x, y):
        """Rysuje pasek XP."""
        current_xp = player.level_manager.current_xp
        xp_per_level = player.level_manager.xp_per_level

        # Tekst
        xp_text = self.font_medium.render(
            f"XP: {int(current_xp)}/{int(xp_per_level)}",
            True,
            self.color_text
        )
        screen.blit(xp_text, (x, y))

        # Pasek XP
        bar_y = y + 30
        self._draw_bar(
            screen,
            x,
            bar_y,
            current_xp,
            xp_per_level,
            self.color_xp_bar,
            self.color_xp_bg
        )

    def _draw_weapons(self, screen, player, x, y):
        """Rysuje informacje o aktywnych broniach."""
        weapons_text = self.font_medium.render("Bronie:", True, self.color_text)
        screen.blit(weapons_text, (x, y))

        y += 30
        weapon_names = []

        # Sprawdź jakie bronie są aktywne
        if player.available_weapons["laser"] is not None:
            weapon_names.append("⚡ Laser")
        if player.available_weapons["shield"] is not None:
            weapon_names.append("🛡️ Tarcza")
        if len(player.active_weapons) > 1 or (len(player.active_weapons) == 1 and player.available_weapons["laser"] is None and player.available_weapons["shield"] is None):
            weapon_names.append("🔫 Domyślna")

        if not weapon_names:
            weapon_names = ["🔫 Domyślna"]

        for weapon_name in weapon_names:
            weapon_text = self.font_small.render(weapon_name, True, (200, 200, 200))
            screen.blit(weapon_text, (x + 20, y))
            y += 25

    def _draw_bar(self, screen, x, y, current, maximum, color_bar, color_bg):
        """
        Rysuje pasek postępu.

        Args:
            screen: Powierzchnia pygame
            x, y: Pozycja paska
            current: Aktualna wartość
            maximum: Maksymalna wartość
            color_bar: Kolor paska
            color_bg: Kolor tła
        """
        # Tło paska
        bg_rect = pygame.Rect(x, y, self.bar_width, self.bar_height)
        pygame.draw.rect(screen, color_bg, bg_rect)
        pygame.draw.rect(screen, WHITE, bg_rect, 2)

        # Pasek
        if maximum > 0:
            progress = min(1.0, current / maximum)
            bar_width = int(self.bar_width * progress)
            bar_rect = pygame.Rect(x, y, bar_width, self.bar_height)
            pygame.draw.rect(screen, color_bar, bar_rect)

