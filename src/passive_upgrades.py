from enum import Enum


class PassiveUpgradeType(Enum):
    """Typy dostępnych ulepszeń pasywnych."""
    ARMOR = "armor"
    SPEED_BOOST = "speed_boost"
    FIRE_RATE_BOOST = "fire_rate_boost"
    HEALTH_REGEN = "health_regen"
    XP_MULTIPLIER = "xp_multiplier"


class PassiveUpgrade:
    """
    Reprezentuje ulepszenie pasywne, które gracz może wybrać przy awansie.
    Ulepszenia pasywne dają stałe bonusy do statystyk.
    """

    def __init__(self, name, description, upgrade_type, value, icon_path=None):
        """
        Inicjalizuje PassiveUpgrade.

        Args:
            name: Nazwa ulepszenia (np. "Pancerz")
            description: Opis ulepszenia (np. "-10% obrażeń otrzymanych")
            upgrade_type: Typ ulepszenia (PassiveUpgradeType enum)
            value: Wartość efektu (np. 0.9 dla -10% obrażeń)
            icon_path: Ścieżka do ikony ulepszenia (opcjonalnie)
        """
        self.name = name
        self.description = description
        self.upgrade_type = upgrade_type
        self.value = value
        self.icon_path = icon_path

    def __repr__(self):
        return f"PassiveUpgrade({self.name}, {self.upgrade_type.value}, {self.value})"

    def get_display_text(self):
        """Zwraca tekst do wyświetlenia na ekranie."""
        return f"{self.name}\n{self.description}"


# Predefiniowane ulepszenia pasywne
PASSIVE_UPGRADE_POOL = [
    PassiveUpgrade(
        "Pancerz I",
        "-10% obrażeń otrzymanych",
        PassiveUpgradeType.ARMOR,
        0.9
    ),
    PassiveUpgrade(
        "Pancerz II",
        "-20% obrażeń otrzymanych",
        PassiveUpgradeType.ARMOR,
        0.8
    ),
    PassiveUpgrade(
        "Pancerz III",
        "-30% obrażeń otrzymanych",
        PassiveUpgradeType.ARMOR,
        0.7
    ),
    PassiveUpgrade(
        "Przyspieszenie I",
        "+15% prędkości ruchu",
        PassiveUpgradeType.SPEED_BOOST,
        1.15
    ),
    PassiveUpgrade(
        "Przyspieszenie II",
        "+30% prędkości ruchu",
        PassiveUpgradeType.SPEED_BOOST,
        1.3
    ),
    PassiveUpgrade(
        "Przyspieszenie III",
        "+50% prędkości ruchu",
        PassiveUpgradeType.SPEED_BOOST,
        1.5
    ),
    PassiveUpgrade(
        "Szybkostrzelność I",
        "+10% szybkość strzelania",
        PassiveUpgradeType.FIRE_RATE_BOOST,
        1.1
    ),
    PassiveUpgrade(
        "Szybkostrzelność II",
        "+20% szybkość strzelania",
        PassiveUpgradeType.FIRE_RATE_BOOST,
        1.2
    ),
    PassiveUpgrade(
        "Szybkostrzelność III",
        "+40% szybkość strzelania",
        PassiveUpgradeType.FIRE_RATE_BOOST,
        1.4
    ),
    PassiveUpgrade(
        "Regeneracja I",
        "+5 HP na sekundę",
        PassiveUpgradeType.HEALTH_REGEN,
        5
    ),
    PassiveUpgrade(
        "Regeneracja II",
        "+10 HP na sekundę",
        PassiveUpgradeType.HEALTH_REGEN,
        10
    ),
    PassiveUpgrade(
        "Mnożnik XP I",
        "+10% więcej XP",
        PassiveUpgradeType.XP_MULTIPLIER,
        1.1
    ),
    PassiveUpgrade(
        "Mnożnik XP II",
        "+25% więcej XP",
        PassiveUpgradeType.XP_MULTIPLIER,
        1.25
    ),
]

