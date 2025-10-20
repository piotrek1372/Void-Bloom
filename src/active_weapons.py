import math
import os
from src.projectile import Projectile


class LaserProjectile(Projectile):
    """
    Pocisk lasera - szybki i silny, porusza się w kierunku ruchu gracza.
    """

    def __init__(self, x, y, direction_x=1, direction_y=0, speed=500, damage=15):
        """
        Inicjalizuje LaserProjectile.

        Args:
            x: Początkowa pozycja X
            y: Początkowa pozycja Y
            direction_x: Kierunek na osi X
            direction_y: Kierunek na osi Y
            speed: Prędkość pocisku (domyślnie 500)
            damage: Obrażenia (domyślnie 15)
        """
        image_path = os.path.join('assets', 'gfx', 'bullet.png')
        super().__init__(
            x=x,
            y=y - 32,
            image_path=image_path,
            speed=speed,
            damage=damage,
            lifetime=None,
            direction_x=direction_x,
            direction_y=direction_y
        )


class ShieldProjectile(Projectile):
    """
    Pocisk tarczy - krąży wokół gracza w orbicie.
    """

    def __init__(self, x, y, player_x, player_y, angle=0, speed=200, damage=8, orbit_radius=80):
        """
        Inicjalizuje ShieldProjectile.

        Args:
            x: Początkowa pozycja X
            y: Początkowa pozycja Y
            player_x: Pozycja X gracza
            player_y: Pozycja Y gracza
            angle: Kąt orbity w radianach
            speed: Prędkość orbity (domyślnie 200)
            damage: Obrażenia (domyślnie 8)
            orbit_radius: Promień orbity (domyślnie 80)
        """
        image_path = os.path.join('assets', 'gfx', 'bullet.png')
        super().__init__(
            x=x,
            y=y,
            image_path=image_path,
            speed=speed,
            damage=damage,
            lifetime=None,
            direction_x=0,
            direction_y=0
        )
        self.player_x = player_x
        self.player_y = player_y
        self.angle = angle
        self.orbit_radius = orbit_radius
        self.angular_velocity = speed / orbit_radius  # Prędkość kątowa

    def move(self, dt):
        """
        Przesuwa pocisk w orbicie wokół gracza.

        Args:
            dt: Delta czasu od ostatniej klatki
        """
        # Aktualizuj kąt
        self.angle += self.angular_velocity * dt

        # Oblicz nową pozycję na orbicie
        new_x = self.player_x + math.cos(self.angle) * self.orbit_radius
        new_y = self.player_y + math.sin(self.angle) * self.orbit_radius

        # Ustaw nową pozycję
        self.rect.centerx = new_x
        self.rect.centery = new_y

    def update(self, dt, player_x=None, player_y=None):
        """
        Aktualizuje stan pocisku (orbita wokół gracza).

        Args:
            dt: Delta czasu od ostatniej klatki
            player_x: Aktualna pozycja X gracza
            player_y: Aktualna pozycja Y gracza

        Returns:
            True jeśli pocisk powinien być usunięty, False w przeciwnym razie
        """
        # Aktualizuj pozycję gracza, jeśli podana
        if player_x is not None and player_y is not None:
            self.player_x = player_x
            self.player_y = player_y

        self.move(dt)

        # Aktualizuj czas życia
        if self.lifetime is not None:
            self.elapsed_time += dt
            if self.elapsed_time >= self.lifetime:
                return True

        return False


class LaserWeapon:
    """
    Broń laserowa - strzela w kierunku ruchu gracza.
    Szybsze pociski, wyższe obrażenia.
    """

    def __init__(self, player_x, player_y, fire_rate=1.5, damage=15):
        """
        Inicjalizuje LaserWeapon.

        Args:
            player_x: Pozycja X gracza
            player_y: Pozycja Y gracza
            fire_rate: Liczba strzałów na sekundę (domyślnie 1.5)
            damage: Obrażenia (domyślnie 15)
        """
        self.fire_rate = fire_rate
        self.cooldown_duration = 1.0 / fire_rate
        self.cooldown_timer = 0.0
        self.projectiles = []
        self.player_x = player_x
        self.player_y = player_y
        self.damage = damage
        self.last_direction_x = 1
        self.last_direction_y = 0

    def set_direction(self, direction_x, direction_y):
        """
        Ustawia kierunek strzału.

        Args:
            direction_x: Kierunek na osi X
            direction_y: Kierunek na osi Y
        """
        # Znormalizuj kierunek
        length = math.sqrt(direction_x**2 + direction_y**2)
        if length > 0:
            self.last_direction_x = direction_x / length
            self.last_direction_y = direction_y / length

    def update(self, dt, player_x, player_y):
        """
        Aktualizuje broń i zarządza cooldownem.

        Args:
            dt: Delta czasu od ostatniej klatki
            player_x: Aktualna pozycja X gracza
            player_y: Aktualna pozycja Y gracza
        """
        self.player_x = player_x
        self.player_y = player_y

        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt
        else:
            self.shoot()

        for projectile in self.projectiles[:]:
            should_remove = projectile.update(dt)
            if should_remove:
                self.projectiles.remove(projectile)

    def shoot(self):
        """Tworzy nowy pocisk lasera."""
        projectile = LaserProjectile(
            self.player_x,
            self.player_y,
            direction_x=self.last_direction_x,
            direction_y=self.last_direction_y,
            speed=500,
            damage=self.damage
        )
        self.projectiles.append(projectile)
        self.cooldown_timer = self.cooldown_duration

    def get_projectiles(self):
        """Zwraca listę pocisków."""
        return self.projectiles

    def remove_projectile(self, projectile):
        """Usuwa pocisk z listy."""
        if projectile in self.projectiles:
            self.projectiles.remove(projectile)

    def set_damage(self, damage):
        """Ustawia obrażenia dla nowych pocisków."""
        self.damage = damage


class ShieldWeapon:
    """
    Broń tarczy - pociski krążą wokół gracza.
    Niższe obrażenia, ale zawsze aktywna obrona.
    """

    def __init__(self, player_x, player_y, fire_rate=2.0, damage=8, num_projectiles=3):
        """
        Inicjalizuje ShieldWeapon.

        Args:
            player_x: Pozycja X gracza
            player_y: Pozycja Y gracza
            fire_rate: Liczba nowych pocisków na sekundę (domyślnie 2.0)
            damage: Obrażenia (domyślnie 8)
            num_projectiles: Liczba pocisków w orbicie (domyślnie 3)
        """
        self.fire_rate = fire_rate
        self.cooldown_duration = 1.0 / fire_rate
        self.cooldown_timer = 0.0
        self.projectiles = []
        self.player_x = player_x
        self.player_y = player_y
        self.damage = damage
        self.num_projectiles = num_projectiles
        self.orbit_radius = 80

        # Stwórz początkowe pociski
        self._spawn_initial_projectiles()

    def _spawn_initial_projectiles(self):
        """Tworzy początkowe pociski w orbicie."""
        for i in range(self.num_projectiles):
            angle = (2 * math.pi * i) / self.num_projectiles
            projectile = ShieldProjectile(
                self.player_x,
                self.player_y,
                self.player_x,
                self.player_y,
                angle=angle,
                speed=200,
                damage=self.damage,
                orbit_radius=self.orbit_radius
            )
            self.projectiles.append(projectile)

    def update(self, dt, player_x, player_y):
        """
        Aktualizuje broń i zarządza cooldownem.

        Args:
            dt: Delta czasu od ostatniej klatki
            player_x: Aktualna pozycja X gracza
            player_y: Aktualna pozycja Y gracza
        """
        self.player_x = player_x
        self.player_y = player_y

        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt
        else:
            self.shoot()

        for projectile in self.projectiles[:]:
            should_remove = projectile.update(dt, player_x, player_y)
            if should_remove:
                self.projectiles.remove(projectile)

    def shoot(self):
        """Tworzy nowy pocisk w orbicie."""
        angle = (2 * math.pi * len(self.projectiles)) / max(1, self.num_projectiles)
        projectile = ShieldProjectile(
            self.player_x,
            self.player_y,
            self.player_x,
            self.player_y,
            angle=angle,
            speed=200,
            damage=self.damage,
            orbit_radius=self.orbit_radius
        )
        self.projectiles.append(projectile)
        self.cooldown_timer = self.cooldown_duration

    def get_projectiles(self):
        """Zwraca listę pocisków."""
        return self.projectiles

    def remove_projectile(self, projectile):
        """Usuwa pocisk z listy."""
        if projectile in self.projectiles:
            self.projectiles.remove(projectile)

    def set_damage(self, damage):
        """Ustawia obrażenia dla nowych pocisków."""
        self.damage = damage

