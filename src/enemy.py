import os
import math
from src.entity import Entity
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Enemy(Entity):
    """
    Klasa reprezentująca wroga w grze.
    Dziedziczy z Entity i dodaje logikę specyficzną dla wrogów.
    """

    def __init__(self, x, y, image_path=None, health=20, max_velocity_x=80, max_velocity_y=80, acceleration=30):
        """
        Inicjalizuje Enemy.

        Args:
            x: Początkowa pozycja X
            y: Początkowa pozycja Y
            image_path: Ścieżka do pliku obrazu (domyślnie enemy.png)
            health: Punkty zdrowia wroga
            max_velocity_x: Maksymalna prędkość na osi X
            max_velocity_y: Maksymalna prędkość na osi Y
            acceleration: Przyspieszenie
        """
        if image_path is None:
            image_path = os.path.join('assets', 'gfx', 'enemy.png')

        super().__init__(
            x=x,
            y=y,
            image_path=image_path,
            max_velocity_x=max_velocity_x,
            max_velocity_y=max_velocity_y,
            acceleration=acceleration
        )

        # Statystyki wroga
        self.health = health
        self.max_health = health

    def physics(self):
        """Implementuje fizykę specyficzną dla wroga (ograniczenia granic ekranu)."""
        # Ograniczenia poziome
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity_x = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.velocity_x = 0

        # Ograniczenia pionowe
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0

        # Zastosuj ograniczenia prędkości z klasy bazowej
        self.apply_velocity_limits()

    def update(self, dt):
        """
        Aktualizuje stan wroga (fizyka, ruch).

        Args:
            dt: Delta czasu od ostatniej klatki
        """
        self.physics()
        self.move(dt)

    def take_damage(self, damage):
        """
        Zadaje obrażenia wrogowi.

        Args:
            damage: Ilość obrażeń

        Returns:
            True jeśli wróg powinien być usunięty (zdrowotnie <= 0), False w przeciwnym razie
        """
        self.health -= damage
        return self.health <= 0

    def apply_knockback(self, projectile_x, projectile_y, knockback_force=200):
        """
        Stosuje efekt odrzutu wroga w kierunku przeciwnym do pocisku.
        Zwiększa satysfakcję z trafienia.

        Args:
            projectile_x: Pozycja X pocisku
            projectile_y: Pozycja Y pocisku
            knockback_force: Siła odrzutu (domyślnie 200)
        """
        # Oblicz kierunek od pocisku do wroga (kierunek odrzutu)
        dx = self.rect.centerx - projectile_x
        dy = self.rect.centery - projectile_y
        distance = math.sqrt(dx**2 + dy**2)

        # Jeśli dystans > 0, znormalizuj kierunek i zastosuj odrzut
        if distance > 0:
            dx_norm = dx / distance
            dy_norm = dy / distance

            # Zastosuj siłę odrzutu do prędkości
            self.velocity_x += dx_norm * knockback_force
            self.velocity_y += dy_norm * knockback_force

    def is_alive(self):
        """Sprawdza, czy wróg żyje."""
        return self.health > 0

    def move_towards_player(self, player_x, player_y, dt):
        """
        Porusza wroga w kierunku gracza.

        Args:
            player_x: Pozycja X gracza
            player_y: Pozycja Y gracza
            dt: Delta czasu od ostatniej klatki
        """
        # Oblicz kierunek do gracza
        dx = player_x - self.rect.centerx
        dy = player_y - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        # Jeśli dystans > 0, znormalizuj kierunek i zastosuj przyspieszenie
        if distance > 0:
            dx_norm = dx / distance
            dy_norm = dy / distance

            # Zastosuj przyspieszenie w kierunku gracza
            self.velocity_x += dx_norm * self.acc * dt
            self.velocity_y += dy_norm * self.acc * dt

    def is_off_screen(self, screen_width, screen_height):
        """
        Sprawdza, czy wróg wyszedł poza ekran.

        Args:
            screen_width: Szerokość ekranu
            screen_height: Wysokość ekranu

        Returns:
            True jeśli wróg jest poza ekranem, False w przeciwnym razie
        """
        return (self.rect.right < 0 or self.rect.left > screen_width or
                self.rect.bottom < 0 or self.rect.top > screen_height)
