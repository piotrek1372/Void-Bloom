from enum import Enum


class UpgradeType(Enum):
    """Typy dostępnych ulepszeń."""
    DAMAGE = "damage"
    FIRE_RATE = "fire_rate"
    HEALTH = "health"
    SPEED = "speed"
    MAGNET_RANGE = "magnet_range"
    WEAPON = "weapon"  # Zmiana aktywnej broni


class Upgrade:
    """
    Reprezentuje ulepszenie, które gracz może wybrać przy awansie.
    Każde ulepszenie ma nazwę, opis, typ i wartość efektu.
    """

    def __init__(self, name, description, upgrade_type, value, icon_path=None):
        """
        Inicjalizuje Upgrade.

        Args:
            name: Nazwa ulepszenia (np. "Zwiększ obrażenia")
            description: Opis ulepszenia (np. "+20% obrażeń")
            upgrade_type: Typ ulepszenia (UpgradeType enum)
            value: Wartość efektu (np. 1.2 dla +20%)
            icon_path: Ścieżka do ikony ulepszenia (opcjonalnie)
        """
        self.name = name
        self.description = description
        self.upgrade_type = upgrade_type
        self.value = value
        self.icon_path = icon_path

    def __repr__(self):
        return f"Upgrade({self.name}, {self.upgrade_type.value}, {self.value})"

    def get_display_text(self):
        """Zwraca tekst do wyświetlenia na ekranie."""
        return f"{self.name}\n{self.description}"


# Predefiniowane ulepszenia
UPGRADE_POOL = [
    Upgrade(
        "Zwiększ Obrażenia",
        "+20% obrażeń",
        UpgradeType.DAMAGE,
        1.2
    ),
    Upgrade(
        "Zwiększ Obrażenia II",
        "+30% obrażeń",
        UpgradeType.DAMAGE,
        1.3
    ),
    Upgrade(
        "Zwiększ Obrażenia III",
        "+50% obrażeń",
        UpgradeType.DAMAGE,
        1.5
    ),
    Upgrade(
        "Szybsza Strzelanka",
        "+25% szybkość strzelania",
        UpgradeType.FIRE_RATE,
        1.25
    ),
    Upgrade(
        "Szybsza Strzelanka II",
        "+50% szybkość strzelania",
        UpgradeType.FIRE_RATE,
        1.5
    ),
    Upgrade(
        "Szybsza Strzelanka III",
        "+100% szybkość strzelania",
        UpgradeType.FIRE_RATE,
        2.0
    ),
    Upgrade(
        "Zwiększ Zdrowie",
        "+25 HP",
        UpgradeType.HEALTH,
        25
    ),
    Upgrade(
        "Zwiększ Zdrowie II",
        "+50 HP",
        UpgradeType.HEALTH,
        50
    ),
    Upgrade(
        "Zwiększ Zdrowie III",
        "+100 HP",
        UpgradeType.HEALTH,
        100
    ),
    Upgrade(
        "Zwiększ Prędkość",
        "+20% prędkość ruchu",
        UpgradeType.SPEED,
        1.2
    ),
    Upgrade(
        "Zwiększ Prędkość II",
        "+50% prędkość ruchu",
        UpgradeType.SPEED,
        1.5
    ),
    Upgrade(
        "Zwiększ Zasięg Magnesu",
        "+50 px zasięg magnesu XP",
        UpgradeType.MAGNET_RANGE,
        50
    ),
    Upgrade(
        "Zwiększ Zasięg Magnesu II",
        "+100 px zasięg magnesu XP",
        UpgradeType.MAGNET_RANGE,
        100
    ),
    Upgrade(
        "Laser",
        "Szybkie pociski w kierunku ruchu",
        UpgradeType.WEAPON,
        "laser"
    ),
    Upgrade(
        "Tarcza Energetyczna",
        "Pociski krążą wokół Ciebie",
        UpgradeType.WEAPON,
        "shield"
    ),
]

