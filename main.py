import pygame, os
from src.settings import SCREEN, FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from src.player import Player
from src.enemy_manager import EnemyManager
from src.xp_manager import XPManager
from src.upgrade_pool import UpgradePool
from src.level_up_screen import LevelUpScreen
from src.upgrade import UpgradeType
from src.passive_upgrades import PassiveUpgradeType
from src.sound_manager import SoundManager
from src.visual_effects import EffectManager
from src.demo_timer import DemoTimer
from src.game_over_screen import GameOverScreen
from src.player_hud import PlayerHUD
from src.enemy_health_bar import EnemyHealthBarManager
from src.spatial_grid import SpatialGrid
from src.performance_monitor import PerformanceMonitor
from src.parallax_manager import ParallaxManager

pygame.init()
SCREEN

def load_background():
    try:
        background_path = os.path.join('assets', 'gfx', 'parallax-space-background.png')
        return background_path
    except pygame.error as e:
        print(f"Nie można załadować obrazka tła: {background_path}")
        print(e)

def scale_background():
    path = load_background()
    image = pygame.image.load(path).convert()
    image_width = image.get_width()
    image_height = image.get_height()
    scaled_w = SCREEN_WIDTH / image_width
    scaled_h = SCREEN_HEIGHT / image_height
    scale = max(scaled_w, scaled_h)
    image_width *= scale
    image_height *= scale
    return pygame.transform.scale(image, (int(image_width), int(image_height)))
def main():
    clock = pygame.time.Clock()
    run = True
    player = Player()
    enemy_manager = EnemyManager(spawn_distance=150, max_enemies=30)  # Zmniejszono z 50 na 30
    xp_manager = XPManager()
    upgrade_pool = UpgradePool()

    # Inicjalizuj parallax manager zamiast scaled_background
    background_path = os.path.join('assets', 'gfx', 'parallax-space-background.png')
    parallax_manager = ParallaxManager(background_path)

    # Inicjalizuj systemy gry
    sound_manager = SoundManager()
    effect_manager = EffectManager()
    demo_timer = DemoTimer(duration_seconds=600)  # 10 minut
    player_hud = PlayerHUD()
    enemy_health_bar_manager = EnemyHealthBarManager()
    spatial_grid = SpatialGrid(SCREEN_WIDTH, SCREEN_HEIGHT, cell_size=100)
    performance_monitor = PerformanceMonitor(show_debug=True)  # Wyświetlaj FPS i debug info

    # Przekaż sound_manager do gracza
    player.set_sound_manager(sound_manager)

    # Stan gry
    game_paused = False
    level_up_screen = None
    game_over_screen = None
    demo_ended = False
    enemies_killed = 0

    while run:
        dt = clock.tick(FPS) / 1000
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
            # Obsługuj klik myszy na ekranie awansu
            if event.type == pygame.MOUSEBUTTONDOWN and level_up_screen is not None:
                selected_upgrade = level_up_screen.handle_mouse_click(event.pos)
                if selected_upgrade is not None:
                    # Sprawdź typ ulepszenia i zastosuj odpowiednio
                    if hasattr(selected_upgrade, 'upgrade_type'):
                        if isinstance(selected_upgrade.upgrade_type, UpgradeType):
                            player.apply_upgrade(selected_upgrade)
                        elif isinstance(selected_upgrade.upgrade_type, PassiveUpgradeType):
                            player.apply_passive_upgrade(selected_upgrade)
                    game_paused = False
                    level_up_screen = None
            # Obsługuj ruch myszy na ekranie awansu
            if event.type == pygame.MOUSEMOTION and level_up_screen is not None:
                level_up_screen.handle_mouse_motion(event.pos)

        # Rysuj tło z efektem parallax
        parallax_manager.draw_background(SCREEN)

        # Aktualizuj efekty wizualne
        effect_manager.update(dt)

        # Aktualizuj monitor wydajności
        performance_monitor.update(dt)

        # Aktualizuj timer demo
        if not game_paused and not demo_ended:
            if demo_timer.update(dt):
                demo_ended = True
                game_over_screen = GameOverScreen(
                    player_level=player.get_level(),
                    total_xp=player.level_manager.total_xp,
                    enemies_killed=enemies_killed,
                    time_survived=demo_timer.total_duration
                )
                game_paused = True

        # Jeśli gra nie jest wznowiona, nie aktualizuj logiki gry
        if not game_paused and not demo_ended:
            # Aktualizuj gracza
            player.input(keys, dt)
            player.update(dt)

            # Aktualizuj parallax na podstawie ruchu gracza
            parallax_manager.update(player.velocity_x, player.velocity_y, dt)

            player.draw(SCREEN)

            # Aktualizuj wrogów
            enemy_manager.update(dt, player)

            # Sprawdzaj kolizje gracza z wrogami
            for enemy in enemy_manager.get_enemies():
                if player.rect.colliderect(enemy.rect):
                    # Gracz otrzymuje obrażenia od wroga
                    if player.take_damage(1):  # 1 obrażenie na klatkę
                        # Gracz umarł
                        sound_manager.play_enemy_death_sound()
                        game_over_screen = GameOverScreen(
                            player_level=player.get_level(),
                            total_xp=player.level_manager.total_xp,
                            enemies_killed=enemies_killed,
                            time_survived=demo_timer.total_duration
                        )
                        game_paused = True

            # Rysuj wrogów
            for enemy in enemy_manager.get_enemies():
                enemy.draw(SCREEN)

            # Aktualizuj paski zdrowia (obsługuje zanikanie po śmierci)
            enemy_health_bar_manager.update(dt, enemy_manager.get_enemies())

            # Rysuj paski zdrowia wrogów
            enemy_health_bar_manager.draw_all(SCREEN, enemy_manager.get_enemies())

            # Optymalizacja: Przebuduj spatial grid z aktualną listą wrogów
            # Czyść siatkę i dodaj wszystkich żywych wrogów
            spatial_grid.clear()
            for enemy in enemy_manager.get_enemies():
                spatial_grid.add_object(enemy)

            # Rysuj pociski z broni gracza i sprawdzaj kolizje z wrogami
            for projectile in player.get_bullets().copy():
                projectile.draw(SCREEN)

                # Sprawdzaj kolizje z wrogami (używając spatial grid)
                nearby_enemies = spatial_grid.get_nearby_objects(projectile, radius=1)
                for enemy in nearby_enemies:
                    if projectile.rect.colliderect(enemy.rect):
                        # Zadaj obrażenia wrogowi
                        sound_manager.play_hit_sound()
                        effect_manager.add_hit_flash(id(enemy), enemy.rect, duration=0.1)

                        # Zastosuj efekt odrzutu wroga (Game Feel)
                        enemy.apply_knockback(projectile.rect.centerx, projectile.rect.centery, knockback_force=200)

                        if enemy.take_damage(projectile.damage):
                            # Wróg umarł - spawniaj XP klejnoty
                            sound_manager.play_enemy_death_sound()
                            xp_manager.spawn_gems_from_enemy(
                                enemy.rect.centerx,
                                enemy.rect.centery,
                                num_gems=2,
                                xp_per_gem=10
                            )
                            enemy_manager.remove_enemy(enemy)
                            enemies_killed += 1

                        # Obsługuj piercing - licznik przebić
                        # piercing=True: nieskończone przebicia (np. tarcza)
                        # piercing=False: brak przebić (zwykłe kule)
                        # piercing=liczba: liczba przebić (np. laser z piercing=2)
                        should_remove = False
                        if isinstance(projectile.piercing, bool):
                            # Jeśli piercing to boolean
                            if not projectile.piercing:
                                should_remove = True
                        else:
                            # Jeśli piercing to liczba
                            projectile.piercing_count += 1
                            if projectile.piercing_count >= projectile.piercing:
                                should_remove = True

                        if should_remove and projectile.weapon_source is not None:
                            projectile.weapon_source.remove_projectile(projectile)
                        break

                # Usuń pocisk, jeśli wyszedł poza ekran - używaj weapon_source
                if projectile.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                    if projectile.weapon_source is not None:
                        projectile.weapon_source.remove_projectile(projectile)

            # Aktualizuj klejnoty XP i zbieraj je
            collected_xp, collected_gems = xp_manager.update(dt, player)
            if collected_xp > 0:
                sound_manager.play_xp_pickup_sound()
                # Dodaj efekty wizualne dla zebranych klejnotów
                for gem in collected_gems:
                    effect_manager.add_xp_absorption(gem.rect.centerx, gem.rect.centery, player.rect.centerx, player.rect.centery, duration=0.3)
                level_ups = player.add_xp(collected_xp)
                # Jeśli gracz awansował, pokaż ekran awansu
                if level_ups > 0:
                    sound_manager.play_level_up_sound()
                    effect_manager.add_screen_shake(duration=0.3, intensity=8)
                    current_level = player.get_level()
                    upgrades = upgrade_pool.get_random_upgrades(3)
                    level_up_screen = LevelUpScreen(upgrades, current_level)
                    game_paused = True

            # Rysuj klejnoty XP
            for gem in xp_manager.get_gems():
                gem.draw(SCREEN)
        else:
            # Gra jest wznowiona - rysuj ostatnią klatkę
            player.draw(SCREEN)
            for enemy in enemy_manager.get_enemies():
                enemy.draw(SCREEN)
            for projectile in player.get_bullets():
                projectile.draw(SCREEN)
            for gem in xp_manager.get_gems():
                gem.draw(SCREEN)

        # Rysuj HUD gracza (jeśli gra nie jest wznowiona)
        if not game_paused or level_up_screen is None:
            player_hud.draw(SCREEN, player)

        # Rysuj timer demo
        if not demo_ended:
            demo_timer.draw(SCREEN)

        # Rysuj monitor wydajności (debug info)
        performance_monitor.draw(
            SCREEN,
            enemy_count=len(enemy_manager.get_enemies()),
            projectile_count=len(player.get_bullets()),
            gem_count=len(xp_manager.get_gems())
        )

        # Rysuj ekran awansu, jeśli jest aktywny
        if level_up_screen is not None:
            level_up_screen.draw(SCREEN)

        # Rysuj ekran gry skończonej, jeśli jest aktywny
        if game_over_screen is not None:
            game_over_screen.draw(SCREEN)
            # Obsługuj klik myszy na ekranie gry skończonej
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = game_over_screen.handle_mouse_click(event.pos)
                if action == 'wishlist':
                    import webbrowser
                    webbrowser.open('https://steamcommunity.com/app/2000000000')  # Placeholder Steam link
                elif action == 'exit':
                    run = False
            # Obsługuj ruch myszy na ekranie gry skończonej
            if event.type == pygame.MOUSEMOTION:
                game_over_screen.handle_mouse_motion(event.pos)

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()