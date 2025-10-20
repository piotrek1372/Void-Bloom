class LevelManager:
    """
    Zarządza poziomem gracza, doświadczeniem i progresją.
    Śledzi zebrane XP i oblicza aktualny poziom.
    """

    def __init__(self, xp_per_level=100):
        """
        Inicjalizuje LevelManager.

        Args:
            xp_per_level: Ilość XP potrzebna do awansu na następny poziom
        """
        self.level = 1
        self.current_xp = 0
        self.xp_per_level = xp_per_level
        self.total_xp = 0  # Całkowite XP zebrane w grze
        self.level_up_callbacks = []  # Lista funkcji do wywołania przy awansie

    def add_xp(self, xp_amount):
        """
        Dodaje XP do gracza i sprawdza, czy gracz powinien awansować.

        Args:
            xp_amount: Ilość XP do dodania

        Returns:
            Liczba awansów (0 jeśli brak awansu, >0 jeśli były awanse)
        """
        self.current_xp += xp_amount
        self.total_xp += xp_amount
        level_ups = 0

        # Sprawdzaj, czy gracz powinien awansować
        while self.current_xp >= self.xp_per_level:
            self.current_xp -= self.xp_per_level
            self.level += 1
            level_ups += 1
            self._trigger_level_up()

        return level_ups

    def _trigger_level_up(self):
        """Wywołuje wszystkie zarejestrowane callbacki przy awansie."""
        for callback in self.level_up_callbacks:
            callback(self.level)

    def register_level_up_callback(self, callback):
        """
        Rejestruje funkcję do wywołania przy awansie.

        Args:
            callback: Funkcja do wywołania (otrzyma numer poziomu jako argument)
        """
        self.level_up_callbacks.append(callback)

    def get_level(self):
        """Zwraca aktualny poziom gracza."""
        return self.level

    def get_current_xp(self):
        """Zwraca aktualne XP w obecnym poziomie."""
        return self.current_xp

    def get_xp_to_next_level(self):
        """Zwraca ilość XP potrzebną do następnego poziomu."""
        return self.xp_per_level - self.current_xp

    def get_xp_progress(self):
        """
        Zwraca postęp w procentach (0.0 - 1.0) do następnego poziomu.

        Returns:
            Postęp jako liczba zmiennoprzecinkowa od 0.0 do 1.0
        """
        return self.current_xp / self.xp_per_level

    def get_total_xp(self):
        """Zwraca całkowite XP zebrane w grze."""
        return self.total_xp

    def reset(self):
        """Resetuje gracza do poziomu 1 (bez resetowania total_xp)."""
        self.level = 1
        self.current_xp = 0

    def reset_all(self):
        """Resetuje wszystkie statystyki gracza."""
        self.level = 1
        self.current_xp = 0
        self.total_xp = 0

