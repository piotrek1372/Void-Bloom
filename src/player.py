import pygame
import os
from src.entity import Entity
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.weapon import Weapon
from src.level_manager import LevelManager
from src.upgrade import UpgradeType
from src.passive_upgrades import PassiveUpgradeType
from src.active_weapons import LaserWeapon, ShieldWeapon


class Player(Entity):
    def __init__(self):
        # Inicjalizuj Entity z parametrami gracza
        image_path = os.path.join('assets', 'gfx', 'player.png')
        super().__init__(
            x=SCREEN_WIDTH // 20,
            y=SCREEN_HEIGHT // 2 - 32,  # Przybliżona wysokość gracza
            image_path=image_path,
            max_velocity_x=120,
            max_velocity_y=50,
            acceleration=45
        )

        # Inicjalizuj broń z fire_rate = 1.0 (1 strzał na sekundę)
        self.weapon = Weapon(self.rect.centerx, self.rect.centery, fire_rate=1.0)

        # Inicjalizuj system poziomów i XP
        self.level_manager = LevelManager(xp_per_level=100)

        # Statystyki gracza (dla ulepszeń)
        self.base_damage = 10
        self.damage_multiplier = 1.0
        self.fire_rate_multiplier = 1.0
        self.health = 100
        self.max_health = 100
        self.speed_multiplier = 1.0
        self.magnet_range = 150  # Początkowy zasięg magnesu XP
        self.upgrades_applied = []  # Historia zastosowanych ulepszeń

        # Systemy broni
        self.active_weapons = [self.weapon]  # Lista aktywnych broni
        self.current_weapon_index = 0  # Indeks aktualnie używanej broni
        self.available_weapons = {
            "default": self.weapon,
            "laser": None,
            "shield": None
        }

        # Ulepszenia pasywne
        self.armor_multiplier = 1.0  # Mnożnik obrażeń otrzymanych
        self.health_regen = 0.0  # HP na sekundę
        self.xp_multiplier = 1.0  # Mnożnik XP
        self.passive_upgrades = []  # Historia zastosowanych ulepszeń pasywnych
    def input(self, keys, dt):
        if keys[pygame.K_d]:
            self.velocity_x += self.acc * dt
        elif keys[pygame.K_a]:
            self.velocity_x -= self.acc * dt
        else:
            if self.velocity_x > 0:
                self.velocity_x -= self.acc * dt
                if self.velocity_x < 1:
                    self.velocity_x = 0
            elif self.velocity_x < 0:
                self.velocity_x += self.acc * dt
                if self.velocity_x > -1:
                    self.velocity_x = 0
        if keys[pygame.K_w]:
            self.velocity_y -= self.acc * dt
        elif keys[pygame.K_s]:
            self.velocity_y += self.acc * dt
        else:
            if self.velocity_y > 0:
                self.velocity_y -= self.acc * dt
                if self.velocity_y < 1:
                    self.velocity_y = 0
            elif self.velocity_y < 0:
                self.velocity_y += self.acc * dt
                if self.velocity_y > -1:
                    self.velocity_y = 0

    def physics(self):
        """Implementuje fizykę specyficzną dla gracza (ograniczenia granic ekranu)."""
        # Ograniczenia poziome (gracz może być tylko na lewej połowie ekranu)
        if self.rect.left < SCREEN_WIDTH // 20:
            self.rect.left = SCREEN_WIDTH // 20
            self.velocity_x = 0
        elif self.rect.right > SCREEN_WIDTH // 2:
            self.rect.right = SCREEN_WIDTH // 2
            self.velocity_x = 0

        # Ograniczenia pionowe
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Zastosuj ograniczenia prędkości z klasy bazowej
        self.apply_velocity_limits()
    def update(self, dt):
        """
        Aktualizuje stan gracza (fizyka, ruch, broń).

        Args:
            dt: Delta czasu od ostatniej klatki
        """
        self.physics()
        self.move(dt)
        self.update_weapon(dt)

        # Regeneracja zdrowia
        if self.health_regen > 0:
            self.health = min(self.health + self.health_regen * dt, self.max_health)

    def update_weapon(self, dt):
        """Aktualizuje wszystkie aktywne bronie gracza."""
        for weapon in self.active_weapons:
            weapon.update(dt, self.rect.centerx, self.rect.centery)

    def get_bullets(self):
        """Zwraca listę pocisków ze wszystkich aktywnych broni."""
        all_bullets = []
        for weapon in self.active_weapons:
            all_bullets.extend(weapon.get_projectiles())
        return all_bullets

    def add_xp(self, xp_amount):
        """
        Dodaje XP do gracza.

        Args:
            xp_amount: Ilość XP do dodania

        Returns:
            Liczba awansów
        """
        return self.level_manager.add_xp(xp_amount)

    def get_level(self):
        """Zwraca aktualny poziom gracza."""
        return self.level_manager.get_level()

    def get_current_xp(self):
        """Zwraca aktualne XP w obecnym poziomie."""
        return self.level_manager.get_current_xp()

    def get_xp_to_next_level(self):
        """Zwraca ilość XP potrzebną do następnego poziomu."""
        return self.level_manager.get_xp_to_next_level()

    def get_xp_progress(self):
        """Zwraca postęp w procentach (0.0 - 1.0) do następnego poziomu."""
        return self.level_manager.get_xp_progress()

    def get_total_xp(self):
        """Zwraca całkowite XP zebrane w grze."""
        return self.level_manager.get_total_xp()

    def apply_upgrade(self, upgrade):
        """
        Zastosuj ulepszenie do gracza.

        Args:
            upgrade: Obiekt Upgrade do zastosowania
        """
        if upgrade.upgrade_type == UpgradeType.DAMAGE:
            self.damage_multiplier *= upgrade.value
            # Aktualizuj obrażenia wszystkich broni
            new_damage = self.get_damage()
            for weapon in self.active_weapons:
                weapon.set_damage(new_damage)
        elif upgrade.upgrade_type == UpgradeType.FIRE_RATE:
            self.fire_rate_multiplier *= upgrade.value
            # Aktualizuj fire_rate wszystkich broni
            for weapon in self.active_weapons:
                weapon.fire_rate *= upgrade.value
                weapon.cooldown_duration = 1.0 / weapon.fire_rate
        elif upgrade.upgrade_type == UpgradeType.HEALTH:
            self.max_health += upgrade.value
            self.health = self.max_health  # Pełne leczenie przy awansie
        elif upgrade.upgrade_type == UpgradeType.SPEED:
            self.speed_multiplier *= upgrade.value
            self.max_velocity_x *= upgrade.value
            self.max_velocity_y *= upgrade.value
        elif upgrade.upgrade_type == UpgradeType.MAGNET_RANGE:
            self.magnet_range += upgrade.value
        elif upgrade.upgrade_type == UpgradeType.WEAPON:
            # Dodaj nową broń
            self.add_weapon(upgrade.value)

        self.upgrades_applied.append(upgrade)

    def get_damage(self):
        """Zwraca obrażenia z uwzględnieniem mnożnika."""
        return int(self.base_damage * self.damage_multiplier)

    def get_upgrades_count(self):
        """Zwraca liczbę zastosowanych ulepszeń."""
        return len(self.upgrades_applied)

    def get_magnet_range(self):
        """Zwraca aktualny zasięg magnesu XP."""
        return self.magnet_range

    def add_weapon(self, weapon_type):
        """
        Dodaje nową broń do aktywnych broni.

        Args:
            weapon_type: Typ broni ("laser" lub "shield")
        """
        if weapon_type == "laser":
            if self.available_weapons["laser"] is None:
                laser = LaserWeapon(
                    self.rect.centerx,
                    self.rect.centery,
                    fire_rate=1.5,
                    damage=self.get_damage()
                )
                self.available_weapons["laser"] = laser
                self.active_weapons.append(laser)
        elif weapon_type == "shield":
            if self.available_weapons["shield"] is None:
                shield = ShieldWeapon(
                    self.rect.centerx,
                    self.rect.centery,
                    fire_rate=2.0,
                    damage=8,
                    num_projectiles=3
                )
                self.available_weapons["shield"] = shield
                self.active_weapons.append(shield)

    def apply_passive_upgrade(self, passive_upgrade):
        """
        Zastosuj ulepszenie pasywne do gracza.

        Args:
            passive_upgrade: Obiekt PassiveUpgrade do zastosowania
        """
        if passive_upgrade.upgrade_type == PassiveUpgradeType.ARMOR:
            self.armor_multiplier *= passive_upgrade.value
        elif passive_upgrade.upgrade_type == PassiveUpgradeType.SPEED_BOOST:
            self.speed_multiplier *= passive_upgrade.value
            self.max_velocity_x *= passive_upgrade.value
            self.max_velocity_y *= passive_upgrade.value
        elif passive_upgrade.upgrade_type == PassiveUpgradeType.FIRE_RATE_BOOST:
            self.fire_rate_multiplier *= passive_upgrade.value
            # Aktualizuj fire_rate wszystkich broni
            for weapon in self.active_weapons:
                weapon.fire_rate *= passive_upgrade.value
                weapon.cooldown_duration = 1.0 / weapon.fire_rate
        elif passive_upgrade.upgrade_type == PassiveUpgradeType.HEALTH_REGEN:
            self.health_regen += passive_upgrade.value
        elif passive_upgrade.upgrade_type == PassiveUpgradeType.XP_MULTIPLIER:
            self.xp_multiplier *= passive_upgrade.value

        self.passive_upgrades.append(passive_upgrade)

    def take_damage(self, damage):
        """
        Gracz otrzymuje obrażenia z uwzględnieniem pancerza.

        Args:
            damage: Ilość obrażeń
        """
        actual_damage = int(damage * self.armor_multiplier)
        self.health -= actual_damage
        return self.health <= 0  # Zwróć True jeśli gracz umarł

    def is_alive(self):
        """Sprawdza, czy gracz żyje."""
        return self.health > 0