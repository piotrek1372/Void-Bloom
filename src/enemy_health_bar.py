import pygame
from src.settings import WHITE, RED, GREEN


class EnemyHealthBar:
    """
    Wyświetla pasek zdrowia nad wrogiem.
    """

    def __init__(self, bar_width=40, bar_height=5, offset_y=-15, fade_out_duration=0.5):
        """
        Inicjalizuje EnemyHealthBar.

        Args:
            bar_width: Szerokość paska (domyślnie 40)
            bar_height: Wysokość paska (domyślnie 5)
            offset_y: Offset Y od górnej krawędzi wroga (domyślnie -15)
            fade_out_duration: Czas zanikania paska po śmierci wroga w sekundach (domyślnie 0.5)
        """
        self.bar_width = bar_width
        self.bar_height = bar_height
        self.offset_y = offset_y
        self.color_bg = (50, 50, 50)
        self.color_bar = GREEN
        self.color_border = WHITE
        self.fade_out_duration = fade_out_duration
        self.fade_out_timer = 0.0  # Timer dla każdego wroga (będzie przechowywany w słowniku)

    def draw(self, screen, enemy, fade_out_timer=None):
        """
        Rysuje pasek zdrowia wroga.
        Jeśli wróg jest martwy, pasek zanika przez fade_out_duration sekund.

        Args:
            screen: Powierzchnia pygame do rysowania
            enemy: Obiekt wroga
            fade_out_timer: Timer zanikania dla martwego wroga (None jeśli żywy)
        """
        # Jeśli wróg jest żywy, rysuj normalnie
        if enemy.health > 0:
            fade_out_timer = None

        # Jeśli wróg jest martwy i timer zanikania wygasł, nie rysuj
        if fade_out_timer is None and enemy.health <= 0:
            return

        # Oblicz pozycję paska (nad wrogiem)
        bar_x = enemy.rect.centerx - self.bar_width // 2
        bar_y = enemy.rect.top + self.offset_y

        # Oblicz przezroczystość dla zanikającego paska
        alpha = 255
        if fade_out_timer is not None and enemy.health <= 0:
            # Oblicz procent zanikania (od 1.0 do 0.0)
            fade_progress = fade_out_timer / self.fade_out_duration
            alpha = int(255 * fade_progress)

        # Tło paska
        bg_rect = pygame.Rect(bar_x, bar_y, self.bar_width, self.bar_height)
        self._draw_rect_with_alpha(screen, self.color_bg, bg_rect, alpha)
        self._draw_rect_with_alpha(screen, self.color_border, bg_rect, alpha, fill=False)

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
            self._draw_rect_with_alpha(screen, color, health_rect, alpha)

    def _draw_rect_with_alpha(self, screen, color, rect, alpha, fill=True):
        """
        Rysuje prostokąt z przezroczystością.

        Args:
            screen: Powierzchnia pygame do rysowania
            color: Kolor RGB
            rect: Prostokąt do narysowania
            alpha: Przezroczystość (0-255)
            fill: Czy wypełnić prostokąt (True) czy tylko obramowanie (False)
        """
        # Utwórz tymczasową powierzchnię z przezroczystością
        surface = pygame.Surface((rect.width, rect.height))
        surface.set_colorkey((0, 0, 0))
        surface.fill((0, 0, 0))

        if fill:
            pygame.draw.rect(surface, color, (0, 0, rect.width, rect.height))
        else:
            pygame.draw.rect(surface, color, (0, 0, rect.width, rect.height), 1)

        surface.set_alpha(alpha)
        screen.blit(surface, (rect.x, rect.y))


class EnemyHealthBarManager:
    """
    Zarządza paskami zdrowia dla wszystkich wrogów.
    Obsługuje zanikanie paska po śmierci wroga.
    """

    def __init__(self):
        """Inicjalizuje EnemyHealthBarManager."""
        self.health_bar = EnemyHealthBar()
        self.fade_out_timers = {}  # Słownik: id(enemy) -> fade_out_timer

    def update(self, dt, enemies):
        """
        Aktualizuje timery zanikania dla martwych wrogów.

        Args:
            dt: Delta czasu od ostatniej klatki
            enemies: Lista wrogów
        """
        # Aktualizuj timery dla martwych wrogów
        enemy_ids_to_remove = []
        for enemy_id, timer in self.fade_out_timers.items():
            timer -= dt
            if timer <= 0:
                enemy_ids_to_remove.append(enemy_id)
            else:
                self.fade_out_timers[enemy_id] = timer

        # Usuń wygasłe timery
        for enemy_id in enemy_ids_to_remove:
            del self.fade_out_timers[enemy_id]

        # Dodaj nowe timery dla wrogów, którzy właśnie umarli
        for enemy in enemies:
            enemy_id = id(enemy)
            if enemy.health <= 0 and enemy_id not in self.fade_out_timers:
                self.fade_out_timers[enemy_id] = self.health_bar.fade_out_duration

    def draw_all(self, screen, enemies):
        """
        Rysuje paski zdrowia dla wszystkich wrogów.
        Paski martwych wrogów zanikają przez krótki czas.

        Args:
            screen: Powierzchnia pygame do rysowania
            enemies: Lista wrogów
        """
        for enemy in enemies:
            enemy_id = id(enemy)
            fade_out_timer = self.fade_out_timers.get(enemy_id, None)
            self.health_bar.draw(screen, enemy, fade_out_timer)

