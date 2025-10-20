from src.projectile import Bullet


class Weapon:
    """
    Klasa reprezentująca broń gracza.
    Zarządza tworzeniem i aktualizacją pocisków.
    """

    def __init__(self, player_x, player_y, fire_rate=1.0, projectile_class=Bullet, projectile_config=None, damage=10, name="Domyślna"):
        """
        Inicjalizuje broń.

        Args:
            player_x: Pozycja X gracza
            player_y: Pozycja Y gracza
            fire_rate: Liczba strzałów na sekundę (domyślnie 1.0)
            projectile_class: Klasa pocisku do tworzenia (domyślnie Bullet)
            projectile_config: Słownik z konfiguracją pocisku (speed, damage, lifetime, itp.)
            damage: Obrażenia pocisku (domyślnie 10)
            name: Nazwa broni (domyślnie "Domyślna")
        """
        self.name = name
        self.fire_rate = fire_rate  # Strzały na sekundę
        self.cooldown_duration = 1.0 / fire_rate  # Czas między strzałami
        self.cooldown_timer = 0.0
        self.projectiles = []
        self.player_x = player_x
        self.player_y = player_y
        self.damage = damage

        # Konfiguracja pocisku
        self.projectile_class = projectile_class
        self.projectile_config = projectile_config or {}
        self.projectile_config['damage'] = damage

        # Sound manager (będzie ustawiony później)
        self.sound_manager = None

    def update(self, dt, player_x, player_y, velocity_x=0, velocity_y=0):
        """
        Aktualizuje broń i zarządza cooldownem.

        Args:
            dt: Delta czasu od ostatniej klatki
            player_x: Aktualna pozycja X gracza
            player_y: Aktualna pozycja Y gracza
            velocity_x: Prędkość gracza na osi X (opcjonalnie)
            velocity_y: Prędkość gracza na osi Y (opcjonalnie)
        """
        self.player_x = player_x
        self.player_y = player_y

        # Zmniejsz cooldown
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt
        else:
            # Jeśli cooldown skończył się, strzelaj automatycznie
            self.shoot()

        # Aktualizuj pociski
        for projectile in self.projectiles[:]:
            should_remove = projectile.update(dt)
            if should_remove:
                self.projectiles.remove(projectile)

    def set_sound_manager(self, sound_manager):
        """
        Ustawia sound_manager dla broni.

        Args:
            sound_manager: Obiekt SoundManager
        """
        self.sound_manager = sound_manager

    def shoot(self):
        """Tworzy nowy pocisk na pozycji gracza z konfiguracją."""
        # Odtwórz dźwięk strzału
        if self.sound_manager is not None:
            self.sound_manager.play_shoot_sound()

        config = self.projectile_config.copy()
        config['weapon_source'] = self
        projectile = self.projectile_class(self.player_x, self.player_y, **config)
        self.projectiles.append(projectile)
        self.cooldown_timer = self.cooldown_duration

    def get_projectiles(self):
        """Zwraca listę pocisków."""
        return self.projectiles

    def get_bullets(self):
        """Zwraca listę pocisków (alias dla kompatybilności wstecznej)."""
        return self.projectiles

    def remove_projectile(self, projectile):
        """Usuwa pocisk z listy."""
        if projectile in self.projectiles:
            self.projectiles.remove(projectile)

    def remove_bullet(self, bullet):
        """Usuwa pocisk z listy (alias dla kompatybilności wstecznej)."""
        self.remove_projectile(bullet)

    def set_damage(self, damage):
        """
        Ustawia obrażenia dla nowych pocisków.

        Args:
            damage: Nowa wartość obrażeń
        """
        self.damage = damage
        self.projectile_config['damage'] = damage