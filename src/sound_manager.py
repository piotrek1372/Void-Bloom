import pygame
import os


class SoundManager:
    """
    Zarządza wszystkimi dźwiękami w grze.
    Obsługuje efekty dźwiękowe i muzykę.
    """

    def __init__(self):
        """Inicjalizuje SoundManager."""
        pygame.mixer.init()
        self.sounds = {}
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self._load_sounds()

    def _load_sounds(self):
        """Ładuje wszystkie dźwięki z folderu assets/sfx."""
        sfx_dir = os.path.join('assets', 'sfx')

        # Definiuj dostępne dźwięki
        sound_files = {
            'hit': 'hit.wav',
            'enemy_death': 'enemy_death.wav',
            'xp_pickup': 'xp_pickup.wav',
            'level_up': 'level_up.wav',
            'shoot': 'shoot.wav',
        }

        # Spróbuj załadować każdy dźwięk
        for sound_name, filename in sound_files.items():
            filepath = os.path.join(sfx_dir, filename)
            try:
                if os.path.exists(filepath):
                    self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                    self.sounds[sound_name].set_volume(self.sfx_volume)
                else:
                    # Utwórz dummy sound jeśli plik nie istnieje
                    self.sounds[sound_name] = None
            except Exception as e:
                print(f"Nie można załadować dźwięku {filename}: {e}")
                self.sounds[sound_name] = None

    def play_sound(self, sound_name):
        """
        Odtwarza dźwięk.

        Args:
            sound_name: Nazwa dźwięku do odtworzenia
        """
        if sound_name in self.sounds and self.sounds[sound_name] is not None:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Błąd podczas odtwarzania dźwięku {sound_name}: {e}")

    def play_hit_sound(self):
        """Odtwarza dźwięk trafienia."""
        self.play_sound('hit')

    def play_enemy_death_sound(self):
        """Odtwarza dźwięk śmierci wroga."""
        self.play_sound('enemy_death')

    def play_xp_pickup_sound(self):
        """Odtwarza dźwięk podniesienia XP."""
        self.play_sound('xp_pickup')

    def play_level_up_sound(self):
        """Odtwarza dźwięk awansu na poziom."""
        self.play_sound('level_up')

    def play_shoot_sound(self):
        """Odtwarza dźwięk strzału."""
        self.play_sound('shoot')

    def set_sfx_volume(self, volume):
        """
        Ustawia głośność efektów dźwiękowych.

        Args:
            volume: Głośność (0.0 - 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            if sound is not None:
                sound.set_volume(self.sfx_volume)

    def stop_all(self):
        """Zatrzymuje wszystkie dźwięki."""
        pygame.mixer.stop()

