import random
from src.upgrade import UPGRADE_POOL
from src.passive_upgrades import PASSIVE_UPGRADE_POOL


class UpgradePool:
    """
    Zarządza pulą dostępnych ulepszeń i wyborem losowych ulepszeń dla gracza.
    Łączy zarówno ulepszenia aktywne (bronie) jak i pasywne.
    """

    def __init__(self, pool=None, passive_pool=None):
        """
        Inicjalizuje UpgradePool.

        Args:
            pool: Lista ulepszeń aktywnych do użycia (domyślnie UPGRADE_POOL)
            passive_pool: Lista ulepszeń pasywnych do użycia (domyślnie PASSIVE_UPGRADE_POOL)
        """
        self.pool = pool if pool is not None else UPGRADE_POOL
        self.passive_pool = passive_pool if passive_pool is not None else PASSIVE_UPGRADE_POOL
        self.combined_pool = self.pool + self.passive_pool
        self.selected_upgrades = []

    def get_random_upgrades(self, count=3):
        """
        Zwraca losowe ulepszenia z połączonej puli (aktywne + pasywne).

        Args:
            count: Liczba ulepszeń do wybrania (domyślnie 3)

        Returns:
            Lista losowych ulepszeń
        """
        if len(self.combined_pool) < count:
            # Jeśli pula ma mniej ulepszeń niż żądane, zwróć wszystkie
            return self.combined_pool.copy()

        # Wybierz losowe ulepszenia bez powtórzeń
        self.selected_upgrades = random.sample(self.combined_pool, count)
        return self.selected_upgrades

    def get_selected_upgrades(self):
        """Zwraca ostatnio wybrane ulepszenia."""
        return self.selected_upgrades

    def clear_selection(self):
        """Czyści listę wybranych ulepszeń."""
        self.selected_upgrades = []

