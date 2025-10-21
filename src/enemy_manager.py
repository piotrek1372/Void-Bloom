import random
import math
from src.enemy import Enemy
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class EnemyManager:
    """
    Zarządza wrogami w grze, w tym ich spawnowaniem, aktualizacją i usuwaniem.
    Implementuje system fal wrogów, które rosną w trudności wraz z czasem.
    """

    def __init__(self, spawn_distance=100, max_enemies=50):
        """
        Inicjalizuje EnemyManager.

        Args:
            spawn_distance: Dystans od gracza, w którym spawniają się wrogowie (poza ekranem)
            max_enemies: Maksymalna liczba wrogów na ekranie (domyślnie 50)
        """
        self.enemies = []
        self.spawn_distance = spawn_distance
        self.max_enemies = max_enemies
        self.wave = 0
        self.time_elapsed = 0.0
        self.spawn_timer = 0.0
        self.spawn_interval = 1.5  # Początkowy interwał spawnu (sekundy) - zwiększono dla mniejszej liczby wrogów
        self.enemies_per_wave = 2  # Liczba wrogów na falę - zmniejszono z 3 na 2
        self.enemies_spawned = 0

    def update(self, dt, player):
        """
        Aktualizuje wszystkich wrogów i zarządza spawnowaniem nowych.

        Args:
            dt: Delta czasu od ostatniej klatki
            player: Obiekt gracza (do obliczania kierunku wrogów)
        """
        self.time_elapsed += dt
        self.spawn_timer += dt

        # Zwiększaj trudność co 30 sekund, ale z bardziej płynną krzywą
        # Używamy logarytmicznej funkcji zamiast liniowej, aby uniknąć gwałtownych skoków
        if self.time_elapsed > 30 * (self.wave + 1):
            self.wave += 1
            # Logarytmiczna krzywa dla interwału spawnu (zmniejsza się wolniej)
            # log(wave + 1) zapobiega zbyt szybkiemu zmniejszaniu się interwału
            self.spawn_interval = max(0.3, 1.0 - math.log(self.wave + 1) * 0.15)
            # Logarytmiczna krzywa dla liczby wrogów (rośnie wolniej)
            self.enemies_per_wave = 3 + int(math.log(self.wave + 1) * 2)

        # Spawnuj nowych wrogów (jeśli nie osiągnęliśmy limitu)
        if self.spawn_timer >= self.spawn_interval and len(self.enemies) < self.max_enemies:
            self._spawn_enemies(player)
            self.spawn_timer = 0.0

        # Aktualizuj wszystkich wrogów
        for enemy in self.enemies:
            enemy.move_towards_player(player.rect.centerx, player.rect.centery, dt)
            enemy.update(dt)

        # Usuń martwych wrogów
        self.enemies = [enemy for enemy in self.enemies if enemy.is_alive()]

    def _spawn_enemies(self, player):
        """
        Spawnia nowych wrogów wokół gracza.

        Args:
            player: Obiekt gracza (do obliczania pozycji spawnu)
        """
        for _ in range(self.enemies_per_wave):
            # Losuj kąt spawnu (0-360 stopni)
            angle = random.uniform(0, 2 * math.pi)

            # Oblicz pozycję spawnu poza ekranem
            spawn_x = player.rect.centerx + math.cos(angle) * self.spawn_distance
            spawn_y = player.rect.centery + math.sin(angle) * self.spawn_distance

            # Utwórz nowego wroga
            enemy = Enemy(spawn_x, spawn_y)
            self.enemies.append(enemy)
            self.enemies_spawned += 1

    def get_enemies(self):
        """
        Zwraca listę wszystkich wrogów.

        Returns:
            Lista wrogów
        """
        return self.enemies

    def remove_enemy(self, enemy):
        """
        Usuwa wroga z listy.

        Args:
            enemy: Wróg do usunięcia
        """
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def get_wave(self):
        """Zwraca numer aktualnej fali."""
        return self.wave

    def get_enemies_count(self):
        """Zwraca liczbę aktualnie żywych wrogów."""
        return len(self.enemies)

    def get_spawn_interval(self):
        """Zwraca aktualny interwał spawnu."""
        return self.spawn_interval

