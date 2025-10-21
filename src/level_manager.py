class LevelManager:
    """
    Zarządza poziomem gracza, doświadczeniem i progresją.
    Śledzi zebrane XP i oblicza aktualny poziom.
    """

    def __init__(self, xp_per_level=100):
        """
        Inicjalizuje LevelManager.

        Args:
            xp_per_level: Ilość XP potrzebna do awansu na poziom 2 (bazowa wartość)
        """
        self.level = 1
        self.current_xp = 0
        self.base_xp_per_level = xp_per_level  # Bazowa wartość XP dla poziomu 2
        self.total_xp = 0  # Całkowite XP zebrane w grze
        self.level_up_callbacks = []  # Lista funkcji do wywołania przy awansie

    def _get_xp_for_level(self, level):
        """
        Oblicza ilość XP potrzebną do awansu na dany poziom.
        Każdy kolejny poziom wymaga więcej XP (wzór: base_xp * level^1.1).

        Args:
            level: Numer poziomu, do którego chcemy awansować (2, 3, 4, ...)

        Returns:
            Ilość XP potrzebna do awansu na dany poziom
        """
        if level <= 1:
            return 0
        # Wzór: każdy poziom wymaga więcej XP
        # Poziom 2: base_xp * 2^1.1 ≈ base_xp * 2.14
        # Poziom 3: base_xp * 3^1.1 ≈ base_xp * 3.45
        # Poziom 4: base_xp * 4^1.1 ≈ base_xp * 4.97
        return int(self.base_xp_per_level * (level ** 1.1))

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
        while True:
            xp_needed_for_next_level = self._get_xp_for_level(self.level + 1)
            if self.current_xp >= xp_needed_for_next_level:
                self.current_xp -= xp_needed_for_next_level
                self.level += 1
                level_ups += 1
                self._trigger_level_up()
            else:
                break

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
        xp_needed = self._get_xp_for_level(self.level + 1)
        return xp_needed - self.current_xp

    def get_xp_progress(self):
        """
        Zwraca postęp w procentach (0.0 - 1.0) do następnego poziomu.

        Returns:
            Postęp jako liczba zmiennoprzecinkowa od 0.0 do 1.0
        """
        xp_needed = self._get_xp_for_level(self.level + 1)
        if xp_needed == 0:
            return 0.0
        return self.current_xp / xp_needed

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

