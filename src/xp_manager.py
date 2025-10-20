import random
from src.xp_gem import XPGem
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class XPManager:
    """
    Zarządza klejnotami doświadczenia (XP) w grze.
    Odpowiada za spawnowanie, aktualizację i zbieranie klejnotów.
    """

    def __init__(self):
        """Inicjalizuje XPManager."""
        self.gems = []

    def spawn_gem(self, x, y, xp_value=10):
        """
        Spawnia nowy klejnot XP na podanej pozycji.

        Args:
            x: Pozycja X spawnu
            y: Pozycja Y spawnu
            xp_value: Ilość XP, którą daje klejnot (domyślnie 10)
        """
        gem = XPGem(x, y, xp_value=xp_value)
        self.gems.append(gem)

    def spawn_gems_from_enemy(self, enemy_x, enemy_y, num_gems=1, xp_per_gem=10):
        """
        Spawnia klejnoty wokół martwego wroga.

        Args:
            enemy_x: Pozycja X wroga
            enemy_y: Pozycja Y wroga
            num_gems: Liczba klejnotów do spawnu
            xp_per_gem: XP na każdy klejnot
        """
        for _ in range(num_gems):
            # Losuj pozycję spawnu wokół wroga
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(10, 30)
            spawn_x = enemy_x + distance * (angle ** 0.5)
            spawn_y = enemy_y + distance * ((2 * 3.14159 - angle) ** 0.5)

            self.spawn_gem(spawn_x, spawn_y, xp_value=xp_per_gem)

    def update(self, dt, player):
        """
        Aktualizuje wszystkie klejnoty i zarządza ich zbieraniem.

        Args:
            dt: Delta czasu od ostatniej klatki
            player: Obiekt gracza
        """
        collected_xp = 0

        for gem in self.gems[:]:
            # Aktualizuj klejnot (przyciąganie, ruch)
            gem.update(dt, player.rect.centerx, player.rect.centery)

            # Sprawdzaj, czy klejnot został zebrany
            if gem.is_collected(player.rect):
                collected_xp += gem.xp_value
                self.gems.remove(gem)
            # Usuń klejnot, jeśli wyszedł poza ekran
            elif gem.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.gems.remove(gem)

        return collected_xp

    def get_gems(self):
        """
        Zwraca listę wszystkich klejnotów.

        Returns:
            Lista klejnotów
        """
        return self.gems

    def get_gems_count(self):
        """Zwraca liczbę aktualnie widocznych klejnotów."""
        return len(self.gems)

    def clear_gems(self):
        """Usuwa wszystkie klejnoty z gry."""
        self.gems.clear()

