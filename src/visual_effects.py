import pygame


class VisualEffect:
    """Bazowa klasa dla efektów wizualnych."""

    def __init__(self, duration):
        """
        Inicjalizuje efekt wizualny.

        Args:
            duration: Czas trwania efektu w sekundach
        """
        self.duration = duration
        self.elapsed_time = 0.0
        self.is_active = True

    def update(self, dt):
        """
        Aktualizuje efekt.

        Args:
            dt: Delta czasu od ostatniej klatki

        Returns:
            True jeśli efekt powinien być usunięty, False w przeciwnym razie
        """
        self.elapsed_time += dt
        if self.elapsed_time >= self.duration:
            self.is_active = False
            return True
        return False

    def apply(self, surface):
        """
        Stosuje efekt do powierzchni.

        Args:
            surface: Powierzchnia pygame do modyfikacji
        """
        pass


class HitFlashEffect(VisualEffect):
    """
    Efekt białego mignięcia przy trafieniu.
    Używany dla wrogów i gracza.
    """

    def __init__(self, target_rect, duration=0.1, flash_color=(255, 255, 255)):
        """
        Inicjalizuje efekt mignięcia.

        Args:
            target_rect: Rect obiektu do mignięcia
            duration: Czas trwania efektu
            flash_color: Kolor mignięcia (domyślnie biały)
        """
        super().__init__(duration)
        self.target_rect = target_rect
        self.flash_color = flash_color
        self.flash_surface = pygame.Surface((target_rect.width, target_rect.height))
        self.flash_surface.fill(flash_color)
        self.flash_surface.set_alpha(200)

    def apply(self, screen, original_image):
        """
        Stosuje efekt mignięcia do obrazu.

        Args:
            screen: Ekran pygame
            original_image: Oryginalny obraz obiektu

        Returns:
            Zmodyfikowany obraz z efektem mignięcia
        """
        if not self.is_active:
            return original_image

        # Utwórz kopię oryginalnego obrazu
        flashed_image = original_image.copy()

        # Utwórz białą warstwę
        white_overlay = pygame.Surface(flashed_image.get_size())
        white_overlay.fill(self.flash_color)

        # Oblicz przezroczystość na podstawie czasu
        progress = self.elapsed_time / self.duration
        alpha = int(200 * (1 - progress))  # Zanika z czasem
        white_overlay.set_alpha(alpha)

        # Nałóż białą warstwę
        flashed_image.blit(white_overlay, (0, 0))

        return flashed_image


class ScreenShakeEffect(VisualEffect):
    """
    Efekt wstrząsu ekranu.
    Przydatny dla feedback'u przy otrzymywaniu obrażeń lub potężnych atakach.
    """

    def __init__(self, duration=0.2, intensity=5):
        """
        Inicjalizuje efekt wstrząsu ekranu.

        Args:
            duration: Czas trwania wstrząsu
            intensity: Siła wstrząsu w pikselach
        """
        super().__init__(duration)
        self.intensity = intensity
        self.offset_x = 0
        self.offset_y = 0

    def update(self, dt):
        """
        Aktualizuje efekt wstrząsu.

        Args:
            dt: Delta czasu od ostatniej klatki

        Returns:
            True jeśli efekt powinien być usunięty, False w przeciwnym razie
        """
        result = super().update(dt)

        if self.is_active:
            import random
            # Losowy offset dla wstrząsu
            self.offset_x = random.randint(-self.intensity, self.intensity)
            self.offset_y = random.randint(-self.intensity, self.intensity)
        else:
            self.offset_x = 0
            self.offset_y = 0

        return result

    def get_offset(self):
        """
        Zwraca offset ekranu dla wstrząsu.

        Returns:
            Tuple (offset_x, offset_y)
        """
        return (self.offset_x, self.offset_y)


class EffectManager:
    """
    Zarządza wszystkimi efektami wizualnymi w grze.
    """

    def __init__(self):
        """Inicjalizuje EffectManager."""
        self.effects = []
        self.hit_flashes = {}  # Mapowanie obiektów do ich efektów mignięcia
        self.screen_shake = None

    def add_hit_flash(self, obj_id, target_rect, duration=0.1):
        """
        Dodaje efekt mignięcia dla obiektu.

        Args:
            obj_id: Unikalny identyfikator obiektu
            target_rect: Rect obiektu
            duration: Czas trwania efektu
        """
        effect = HitFlashEffect(target_rect, duration)
        self.hit_flashes[obj_id] = effect
        self.effects.append(effect)

    def add_screen_shake(self, duration=0.2, intensity=5):
        """
        Dodaje efekt wstrząsu ekranu.

        Args:
            duration: Czas trwania wstrząsu
            intensity: Siła wstrząsu
        """
        self.screen_shake = ScreenShakeEffect(duration, intensity)
        self.effects.append(self.screen_shake)

    def update(self, dt):
        """
        Aktualizuje wszystkie efekty.

        Args:
            dt: Delta czasu od ostatniej klatki
        """
        for effect in self.effects[:]:
            if effect.update(dt):
                self.effects.remove(effect)
                # Usuń z hit_flashes jeśli to efekt mignięcia
                for obj_id, eff in list(self.hit_flashes.items()):
                    if eff == effect:
                        del self.hit_flashes[obj_id]
                        break

    def get_screen_shake_offset(self):
        """
        Zwraca offset ekranu dla wstrząsu.

        Returns:
            Tuple (offset_x, offset_y)
        """
        if self.screen_shake is not None and self.screen_shake.is_active:
            return self.screen_shake.get_offset()
        return (0, 0)

    def get_hit_flash(self, obj_id):
        """
        Zwraca efekt mignięcia dla obiektu.

        Args:
            obj_id: Unikalny identyfikator obiektu

        Returns:
            HitFlashEffect lub None
        """
        return self.hit_flashes.get(obj_id)

    def clear(self):
        """Czyści wszystkie efekty."""
        self.effects.clear()
        self.hit_flashes.clear()
        self.screen_shake = None

