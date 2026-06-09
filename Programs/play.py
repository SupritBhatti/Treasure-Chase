import pygame
import CL
import database
import settings
from pygame.locals import *
pygame.init()

pygame.mixer.init()

FONT_NAME = "Comic Sans MS"

def shoot_weapon(weapon, bullet_img,current_frame,app_settings):
    if app_settings["sound"]:
        sound_file = app_settings["weapon_sounds"].get(weapon.name)
        pygame.mixer.Sound(sound_file).play()
    return weapon.shoot(current_frame,bullet_img)
def start_game():
    SCREEN_WIDTH = 1850
    SCREEN_HEIGHT = 1000
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Treasure Chase")

    score = 0

    clock = pygame.time.Clock()

    # Timer setup
    start_ticks = pygame.time.get_ticks()  # Get the initial time
    total_time = 5 * 60 * 1000  # 5 minutes in milliseconds

    timer_rect = pygame.Rect(5,5,65,35)

    font = pygame.font.SysFont(FONT_NAME, 35)
    font = pygame.font.SysFont("Comic Sans MS", 35)
    font2 = pygame.font.SysFont("Calibri", 30)

    text_drawer = CL.Text(screen)

    def pause_screen():
        pause = True
        font = pygame.font.SysFont("Comic Sans MS", 50)
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:  # Press 'p' to resume
                    pause = False

            screen.fill((0, 0, 0))
            text = font.render("Paused", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 400))
            text = font.render("Press 'P' to resume", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height() // 2 - 100))
            pygame.display.update()
            clock.tick(5)

        pygame.event.clear()

    def end_screen(score,text_drawer,screen,clock):
        end = True
        while end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if replay_button_rect.collidepoint(mouse_pos):
                        return 'replay'
                    elif return_button_rect.collidepoint(mouse_pos):
                        return 'menu'

            screen.fill((0, 0, 0))
            text_drawer.draw_centered_text(f"Your Score: {score}", font, (255, 255, 255), SCREEN_WIDTH, SCREEN_HEIGHT - 200)
            text = font.render("You Won!", True,(255,255,255))
            screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 400 ))

            small_font = pygame.font.SysFont("Comic Sans MS", 30)

            replay_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
            return_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 50)

            pygame.draw.rect(screen, (0, 255, 0), replay_button_rect)
            text_drawer.draw_centered_text("Replay", small_font, (0, 0, 0), SCREEN_WIDTH, SCREEN_HEIGHT + 50)

            pygame.draw.rect(screen, (255, 0, 0), return_button_rect)
            text_drawer.draw_centered_text("Return to Main Menu", small_font, (0, 0, 0), SCREEN_WIDTH, SCREEN_HEIGHT + 250)

            pygame.display.update()
            clock.tick(60)

    def time_screen(score,text_drawer,screen,clock):
        time = True
        font = pygame.font.SysFont("Comic Sans MS", 50)
        small_font = pygame.font.SysFont("Comic Sans MS", 30)

        replay_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
        return_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 50)

        while time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if replay_button_rect.collidepoint(mouse_pos):
                        return 'replay'
                    elif return_button_rect.collidepoint(mouse_pos):
                        return 'menu'

            screen.fill((0, 0, 0))
            text_drawer.draw_centered_text(f"Your Score: {score}", font, (237,28,36), SCREEN_WIDTH, SCREEN_HEIGHT - 200)
            text = font.render("You ran out of time!", True,(237,28,36))
            screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 400 ))

            pygame.draw.rect(screen, (255, 0, 0), replay_button_rect)
            text_drawer.draw_centered_text("Replay", small_font, (0, 0, 0), SCREEN_WIDTH, SCREEN_HEIGHT + 50)

            pygame.draw.rect(screen, (255, 0, 0), return_button_rect)
            text_drawer.draw_centered_text("Return to Main Menu", small_font, (0, 0, 0), SCREEN_WIDTH, SCREEN_HEIGHT + 250)

            pygame.display.update()
            clock.tick(60)

    def live_screen(score,text_drawer,screen,clock):
        live = True
        font = pygame.font.SysFont("Comic Sans MS", 50)
        small_font = pygame.font.SysFont("Comic Sans MS", 30)

        replay_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
        return_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 50)

        while live:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if replay_button_rect.collidepoint(mouse_pos):
                        return 'replay'
                    elif return_button_rect.collidepoint(mouse_pos):
                        return 'menu'
                    
            screen.fill((0, 0, 0))
            text_drawer.draw_centered_text(f"Your Score: {score}", font, (237,28,36), SCREEN_WIDTH, SCREEN_HEIGHT - 200)
            text = font.render("You died!", True,(237,28,36))
            screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 400 ))

            pygame.draw.rect(screen, (255, 0, 0), replay_button_rect)
            text_drawer.draw_centered_text("Replay", small_font, (0, 0, 0), SCREEN_WIDTH, SCREEN_HEIGHT + 50)

            pygame.draw.rect(screen, (255, 0, 0), return_button_rect)
            text_drawer.draw_centered_text("Return to main menu", small_font, (0, 0, 0), SCREEN_WIDTH, SCREEN_HEIGHT + 250)

            pygame.display.update()
            clock.tick(60)

    pause_img = pygame.image.load ('pause.png').convert_alpha()
    coin_img = pygame.image.load('Coin.png').convert_alpha()
    player_img = pygame.image.load('Guy.png').convert_alpha()
    plat_1_img = pygame.image.load('plat_1.png').convert_alpha()
    plat_2_img = pygame.image.load('plat_2.png').convert_alpha()
    plat_3_img = pygame.image.load('plat_3.png').convert_alpha()
    bullet_img = pygame.image.load('Bullet.png').convert_alpha()
    start_img = pygame.image.load('Gun.png').convert_alpha()
    enemy_img = pygame.image.load('Enemy.png').convert_alpha()
    finish_line_img = pygame.image.load('finish_line.png').convert_alpha()
    relic_img = pygame.image.load('Gun2.png').convert_alpha()

    pause_button = CL.Button(0,150,pause_img)
    player = CL.Player(player_img,100,100)
    platforms = [
        CL.Platform (plat_1_img,100,200),
        CL.Platform (plat_2_img,220,270),
        CL.Platform (plat_3_img,340,340),
        CL.Platform (plat_3_img,1040,340),
        CL.Platform (plat_3_img,740,340),
        CL.Platform (plat_2_img,600,340)
    ]
    coins = [
        CL.Coin(coin_img,200,100),
        CL.Coin(coin_img,300,150),
        CL.Coin(coin_img,450,200)
    ]
    bullets = []
    
    start = CL.StartWeapon(start_img, player,bullet_img)
    relic = CL.RelicWeapon(relic_img, player,bullet_img)

    import main_menu
    main_menu.player_weapon = database.get_weapon()

    if main_menu.player_weapon == "Relic" and database.has_weapon("Relic"):
        current_weapon = relic
    else:
        current_weapon = start
        main_menu.player_weapon = "Start"  # Ensure the default is Start if relic isn't owned
    
    enemies = [CL.Enemy(enemy_img, 1040,240,3),
               CL.Enemy(enemy_img, 340,240,3)
    ]
    finish_line = CL.FinishLine(finish_line_img, 1150,250)

    is_shooting = False
    current_frame = 0
    
    run = True
    while run:
        app_settings = settings.load_settings()
        if app_settings["sound"]:
          start_weapon_sound = pygame.mixer.Sound("sounds/startShot.mp3")
          relic_weapon_sound = pygame.mixer.Sound("sounds/relicShot.mp3")

        current_frame += 1
        clock.tick(60)
        screen.fill((0,162,232))

        seconds = (pygame.time.get_ticks() - start_ticks)//1000
        remaining_time = total_time - (seconds * 1000)

        minutes = remaining_time // 60000
        seconds = (remaining_time % 60000)//1000

        pygame.draw.rect(screen, (0,0,0), timer_rect)
        
        time_text = f"{minutes}:{seconds:02d}"
        text_drawer.draw_text(time_text, font2, (237,28,36), 10, 10)

        if remaining_time <= 0:
            database.insert_score(score)
            result = time_screen(score, text_drawer, screen, clock)  # Call the end screen function and check if replay is chosen
            if result == 'replay':
                # Reset the game state for replay
                player = CL.Player(player_img, 100, 100)
                enemies = [CL.Enemy(enemy_img, 1040,240,3), CL.Enemy(enemy_img, 340,240,3)]
                coins = [CL.Coin(coin_img,200,100), CL.Coin(coin_img,300,150), CL.Coin(coin_img,450,200)]
                start = CL.StartWeapon(start_img, player,bullet_img)
                relic = CL.RelicWeapon(relic_img, player,bullet_img)
                
                # Correctly set the weapon only if the player actually owns Relic
                if database.has_weapon("Relic") and main_menu.player_weapon == "Relic":
                    current_weapon = relic
                else:
                    current_weapon = start
                    main_menu.player_weapon = "Start"  # Reset to Start if Relic is not owned
                score = 0
                start_ticks = pygame.time.get_ticks()  # Reset the timer
            elif result == 'menu':
                return
                   
        pause_button.draw()
        if pause_button.detect():
            pause_screen()
        
        player.draw()
        
        if player.update() or player.check_collision(platforms, enemies):
            score -= 30

        if player.lives <= 0:
            database.insert_score(score)
            result = live_screen(score, text_drawer, screen, clock)  # Call the end screen function and check if replay is chosen
            if result == 'replay':
                # Reset the game state for replay
                player = CL.Player(player_img, 100, 100)
                enemies = [CL.Enemy(enemy_img, 1040,240,3), CL.Enemy(enemy_img, 340,240,3)]
                coins = [CL.Coin(coin_img,200,100), CL.Coin(coin_img,300,150), CL.Coin(coin_img,450,200)]
                start = CL.StartWeapon(start_img, player,bullet_img)
                relic = CL.RelicWeapon(relic_img, player,bullet_img)
                # Correctly set the weapon only if the player actually owns Relic
                if database.has_weapon("Relic") and main_menu.player_weapon == "Relic":
                    current_weapon = relic
                else:
                    current_weapon = start
                    main_menu.player_weapon = "Start"  # Reset to Start if Relic is not owned
                score = 0
                start_ticks = pygame.time.get_ticks()  # Reset the timer
            elif result == 'menu':
                return

        current_weapon.draw(screen)
        
        for platform in platforms:
            platform.draw_platform()
        
        for coin in coins:
            coin.draw_coin()
            if coin.check(player):
                coins.remove(coin)
                score += 50
        
        for bullet in bullets:
            bullet.update()
            enemy_hit = bullet.check_collision(enemies)
            if enemy_hit:
                enemies.remove(enemy_hit)
                bullets.remove(bullet)
                score = score + 100
            elif bullet.rect.x > SCREEN_WIDTH:
                bullets.remove(bullet)
            else:
                bullet.draw(screen)

        enemies = [enemy for enemy in enemies if enemy.update(player, platforms)]
        for enemy in enemies:
            enemy.draw(screen)

        finish_line.draw(screen)

        if finish_line.check(player):  # Check if player reaches the finish line
            database.insert_score(score)
            result = end_screen(score, text_drawer, screen, clock)  # Call the end screen function and check if replay is chosen
            if result == 'replay':
                # Reset the game state for replay
                player = CL.Player(player_img, 100, 100)
                enemies = [CL.Enemy(enemy_img, 1040,240,3), CL.Enemy(enemy_img, 340,240,3)]
                coins = [CL.Coin(coin_img,200,100), CL.Coin(coin_img,300,150), CL.Coin(coin_img,450,200)]
                start = CL.StartWeapon(start_img, player,bullet_img)
                relic = CL.RelicWeapon(relic_img, player,bullet_img)
                # Correctly set the weapon only if the player actually owns Relic
                if database.has_weapon("Relic") and main_menu.player_weapon == "Relic":
                    current_weapon = relic
                else:
                    current_weapon = start
                    main_menu.player_weapon = "Start"  # Reset to Start if Relic is not owned
                score = 0
                start_ticks = pygame.time.get_ticks()  # Reset the timer
            elif result == 'menu':
                return

        score_text = f"Score: {score}"
        text_drawer.draw_text(score_text, font, (237,28,36), 150, 850)
        lives_text = f"Lives: {player.lives}"
        text_drawer.draw_text(lives_text, font, (237,28,36), 1550, 850)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not is_shooting:
                    bullet = shoot_weapon(current_weapon, bullet_img,current_frame, app_settings)
                    if bullet:
                        bullets.append(bullet)
                is_shooting = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                is_shooting = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.rect.x -= 5
        if keys[pygame.K_d]:
            player.rect.x += 5
        if keys[pygame.K_p]:
            pause_screen()
        elif keys[pygame.K_SPACE] and player.on_ground: #only jumps if player is on solid ground
            player.vel_y = -10
                    
        player.draw()
        pygame.display.update()
        
    pygame.quit()
    quit()
