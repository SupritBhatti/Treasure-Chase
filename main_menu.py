import pygame
import CL
import database
import sqlite3
import settings
import json

pygame.init()
#initilises pygame
SCREEN_WIDTH = 1850#sets the screen width in pixels
SCREEN_HEIGHT = 1000#sets the screen height in pixels
clock = pygame.time.Clock()

coin_rect = pygame.Rect(1645,40,85,45)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#creates a 1850 by 1000 screen
pygame.display.set_caption("Treasure Chase")#gives the window the name "Treasure Chase"

player_weapon = "Start"

app_settings = settings.load_settings()

pygame.mixer.init()  # Initialize sound system

# Load weapon sounds if sound is enabled
weapon_sounds = {}
if app_settings["sound"]:
    for weapon, sound_file in app_settings["weapon_sounds"].items():
        weapon_sounds[weapon] = pygame.mixer.Sound(sound_file)  # Load sound file

# Define game states
MAIN_MENU = "main_menu"
PLAY_MENU = "play_menu"
LEVEL_SELECTION = "level_selection"
SHOP = "shop"
SETTINGS = "settings"

# Initialize the current state
current_state = MAIN_MENU

#loads all images that will be used in the program
play_img = pygame.image.load ('play_button.png').convert_alpha()
shop_img = pygame.image.load ('shop_button.png').convert_alpha()
settings_img = pygame.image.load ('settings_button.png').convert_alpha()
leader_img = pygame.image.load('P.leaderboard_button.png').convert_alpha()
shop_coin_img = pygame.image.load('menu_coin.png').convert_alpha()
#Initilises the Button class
play_button = CL.Button(799, 225, play_img)
shop_button = CL.Button(799, 450, shop_img)
settings_button = CL.Button(799, 675, settings_img)
#sets a font that I may want to use - will be used with the text class
font = pygame.font.SysFont("Comic Sans MS",40)
font_2 = pygame.font.SysFont("Comic Sans MS", 30)
#Initilises the Text class
text_drawer = CL.Text(screen)

con = sqlite3.connect("treasureChase_data.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS high_scores(score INT)")

def insert_score(score):
    cur.execute("INSERT INTO high_scores (score) VALUES (?)", (score,))
    con.commit()

def get_top_5_scores():
    cur.execute("SELECT score FROM high_scores ORDER BY score DESC LIMIT 5")
    scores = cur.fetchall()
    return scores

def display_top_5_scores(screen, text_drawer):
    leader = True
    font_2 = pygame.font.SysFont("Comic Sans MS", 40)
    while leader:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if return_button_rect.collidepoint(mouse_pos):
                    return False
        screen.fill((0, 162, 232))
        top_scores = get_top_5_scores()
        y_offset = 300
        text_drawer.draw_text("Top 5 High Scores:", font, (255,242,0), 780, 150)
        for rank, score in enumerate(top_scores, start=1):
            text_drawer.draw_text(f"{rank}. {score[0]}", font, (255,242,0), 800, y_offset)
            y_offset += 50

        return_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 50)

        pygame.draw.rect(screen, (255, 0, 0), return_button_rect)
        text_drawer.draw_centered_text("Return", font_2, (255, 242, 0), SCREEN_WIDTH, SCREEN_HEIGHT + 250)

        pygame.display.update()
        clock.tick(60)

def display_coin_total(text_drawer):
    total_coins = database.get_coin_total()
    coin_text = f"{total_coins}"
    text_drawer.draw_text(coin_text, font, (255, 201, 14), 1700, 30)

def pl():
    pl = True
    font = pygame.font.SysFont("Comic Sans MS", 40)
    small_font = pygame.font.SysFont("Comic Sans MS", 30)
    while pl:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if level_button_rect.collidepoint(mouse_pos):
                    lvl()
                elif return_button_rect.collidepoint(mouse_pos):
                    return False
                elif leader_button_rect.collidepoint(mouse_pos):
                    display_top_5_scores(screen, text_drawer)
                    
        screen.fill((0, 162, 232))
        text = font.render("Play Menu", True,(255,255,255))
        screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 400 ))

        level_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
        return_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 50)
        leader_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 200, 300, 50)

        pygame.draw.rect(screen, (0, 255, 0), level_button_rect)
        text_drawer.draw_centered_text("Levels", small_font, (255, 242, 0), SCREEN_WIDTH, SCREEN_HEIGHT + 50)

        pygame.draw.rect(screen, (255, 0, 0), return_button_rect)
        text_drawer.draw_centered_text("Return", small_font, (255, 242, 0), SCREEN_WIDTH, SCREEN_HEIGHT + 250)
        
        pygame.draw.rect(screen, (255, 242, 0), leader_button_rect)
        text_drawer.draw_centered_text("Personal Leaderboard", small_font, (237, 28, 36), SCREEN_WIDTH, SCREEN_HEIGHT + 450)
        
        pygame.display.update()
        clock.tick(60)

def lvl():
    import play
    lvl = True
    font = pygame.font.SysFont("Comic Sans MS", 40)
    small_font = pygame.font.SysFont("Comic Sans MS", 30)
    while lvl:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if level1_button_rect.collidepoint(mouse_pos):
                    play.start_game()
                    return True
                elif return_button_rect.collidepoint(mouse_pos):
                    return False
        screen.fill((0, 162, 232))
        text = font.render("Play Menu", True,(255,255,255))
        screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 400 ))

        level1_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
        return_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 50)

        pygame.draw.rect(screen, (0, 255, 0), level1_button_rect)
        text_drawer.draw_centered_text("Level 1", small_font, (255, 242, 0), SCREEN_WIDTH, SCREEN_HEIGHT + 50)

        pygame.draw.rect(screen, (255, 0, 0), return_button_rect)
        text_drawer.draw_centered_text("Return", small_font, (255, 242, 0), SCREEN_WIDTH, SCREEN_HEIGHT + 250)

        pygame.display.update()
        clock.tick(60)

def shop():
    global player_weapon
    shop = True
    player_weapon = "Start"
    start_showcase_img = pygame.image.load('start_showcase.png').convert_alpha()
    start_show = CL.Button(600,350,start_showcase_img)
    relic_showcase_img = pygame.image.load('relic_showcase.png').convert_alpha()
    relic_show = CL.Button(923,350,relic_showcase_img)
    while shop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_show.rect.collidepoint(mouse_pos):
                    start()
                elif start_equip_rect.collidepoint(mouse_pos):
                    equip_weapon("Start")
                elif relic_show.rect.collidepoint(mouse_pos):
                    relic()
                elif relic_equip_rect.collidepoint(mouse_pos):
                    if database.has_weapon("Relic"):
                        equip_weapon("Relic")
                    elif purchase_relic():
                        database.purchase_weapon("Relic")
                        equip_weapon("Relic")
                elif return_button_rect.collidepoint(mouse_pos):
                    return False
        screen.fill((136,0,21))
        start_show.draw()
        relic_show.draw()
        pygame.draw.rect(screen, (136,0,21), coin_rect)
        text = font.render("Shop", True, (255,242,0))
        screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 400 ))
        text = font.render("Buy anything you desire!",True,(255,242,0))
        screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height() // 2 - 300 ))
        
        coins = [CL.Coin(shop_coin_img, 1650, 45)]
        for coin in coins:
            coin.draw_coin()
        display_coin_total(text_drawer)

        return_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 880, SCREEN_HEIGHT // 2 + 330, 120, 45)
        start_equip_rect = pygame.Rect(600,700, 300, 50)
        relic_equip_rect = pygame.Rect(923,700, 300, 50)

        pygame.draw.rect(screen, (0,0,0), return_button_rect)
        text_drawer.draw_centered_text("Return", font_2, (255,242,0), 200, 1700)

        pygame.draw.rect(screen, (0,255,0), start_equip_rect)
        text_drawer.draw_centered_text("Equip Start", font_2, (255,242,0), 1500, 1450)

        pygame.draw.rect(screen, (0,255,0), relic_equip_rect)
        text_drawer.draw_centered_text("Equip Relic", font_2, (255,242,0), 2160, 1450)

        pygame.display.update()
        clock.tick(60)

def start():
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if return_button_rect.collidepoint(mouse_pos):
                    return False
        screen.fill((0,0,0))
        text = font.render("Start", True, (255,255,255))
        screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 400 ))
        text = font.render("Weapon Information: ",True,(255,255,255))
        screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height() // 2 - 300 ))
        text = font.render("The basic starter weapon which you get",True,(255,255,255))
        screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height() // 2 - 200 ))
        text = font.render("Special Abilities: N/A",True,(255,255,255))
        screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height() // 2 - 100 ))

        return_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 50)

        pygame.draw.rect(screen, (255, 0, 0), return_button_rect)
        text_drawer.draw_centered_text("Return", font_2, (255, 242, 0), SCREEN_WIDTH, SCREEN_HEIGHT + 250)

        pygame.display.update()
        clock.tick(60)

def relic():
    relic = True
    while relic:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if return_button_rect.collidepoint(mouse_pos):
                    return False
        screen.fill((0,0,0))
        text = font.render("Relic", True, (255,255,255))
        screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 400 ))
        text = font.render("Weapon Information: ",True,(255,255,255))
        screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height() // 2 - 300 ))
        text = font.render("A vintage weapon with a special shine",True,(255,255,255))
        screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height() // 2 - 200 ))
        text = font.render("Special Abilities: Can pierce through enemies and gain multikills",True,(255,255,255))
        screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height() // 2 - 100 ))

        return_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 50)

        pygame.draw.rect(screen, (255, 0, 0), return_button_rect)
        text_drawer.draw_centered_text("Return", font_2, (255, 242, 0), SCREEN_WIDTH, SCREEN_HEIGHT + 250)

        pygame.display.update()
        clock.tick(60)

def purchase_relic():
    if database.has_weapon("Relic"):#Checks if Relic is already purchased
        return True #Allows user to equip without using coins
    
    current_coins = database.get_coin_total()
    if current_coins >= 150:
        database.insert_coins(-150)
        database.purchase_weapon("Relic")
        return True
    else:
        return False

def equip_weapon(weapon_name):
    global player_weapon
    player_weapon = weapon_name
    database.set_weapon(weapon_name)

def settings_menu():
    global app_settings
    settings_open = True
    font = pygame.font.SysFont("Comic Sans MS", 40)
    toggle_sound_button = pygame.Rect(725, 400, 400, 60)

    while settings_open:
        screen.fill((0, 120, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if return_button_rect.collidepoint(mouse_pos):
                    return False
                elif toggle_sound_button.collidepoint(mouse_pos):
                    app_settings["sound"] = not app_settings["sound"]  # Toggle sound
                    settings.save_settings(app_settings)

                    # Reload settings and update weapon sounds
                    app_settings = settings.load_settings()
                    weapon_sounds.clear()
                    if app_settings["sound"]:
                        for weapon, sound_file in app_settings["weapon_sounds"].items():
                            weapon_sounds[weapon] = pygame.mixer.Sound(sound_file)

        # Draw the button
        pygame.draw.rect(screen, (0, 201, 200), toggle_sound_button)
        sound_status = "ON" if app_settings["sound"] else "OFF"
        text_drawer.draw_centered_text(f"Weapon Sounds: {sound_status}", font, (255, 255, 255), SCREEN_WIDTH, SCREEN_HEIGHT - 400)
        text_drawer.draw_centered_text("Press to toggle sound", font, (0, 120, 0), SCREEN_WIDTH, SCREEN_HEIGHT - 150)

        text = font.render("Settings", True, (255,255,255))
        screen.blit(text,(SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 400 ))

        return_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 880, SCREEN_HEIGHT // 2 + 330, 120, 45)

        pygame.draw.rect(screen, (0, 0, 0), return_button_rect)
        text_drawer.draw_centered_text("Return", font_2, (255, 242, 0), 200, 1700)

        pygame.display.update()
        clock.tick(60)


def toggle_sound():
    app_settings["sound"] = not app_settings["sound"]  # Toggle True/False

    # Save the new setting
    with open("settings.json", "w") as file:
        json.dump(app_settings, file, indent=4)


def main_menu():
    main = True
    while main:
        screen.fill((0, 162, 232))
        
        play_button.draw()
        shop_button.draw()
        settings_button.draw()
        
        text_drawer.draw_text("Treasure Chase", font, (237, 28, 36), 780, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.rect.collidepoint(mouse_pos):
                    pl()
                elif shop_button.rect.collidepoint(mouse_pos):
                    shop()
                elif settings_button.rect.collidepoint(mouse_pos):
                    settings_menu()

        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()
    quit()

def main_loop():
    global current_state
    run = True
    while run:
        if current_state == MAIN_MENU:
            current_state = main_menu()
        elif current_state == PLAY_MENU:
            current_state = pl()
        elif current_state == LEVEL_SELECTION:
            current_state = lvl()
            current_state = MAIN_MENU
        elif current_state == SHOP:
            current_state = shop()
        elif current_state == SETTINGS:
            current_state = settings_menu()
            current_state = MAIN_MENU

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
    quit()

if __name__ == "__main__":
    main_loop()
