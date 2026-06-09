import pygame
import database
from pygame.locals import *
pygame.init()
#initilises pygame
SCREEN_WIDTH = 1850#sets the screen width in pixels
SCREEN_HEIGHT = 1000#sets the screen height in pixels
GRAVITY = 0.5
BULLET_SPEED = 10
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#creates a 1000 by 800 screen
pygame.display.set_caption("Treasure Chase")#gives the window the name "Treasure Chase"


class Button():#Creates the button class
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()#sets the image as a rectangle
        self.rect.topleft = (x, y)#gets the coordinate of the top left pixel of the image
        self.clicked = False

    def draw(self): #allows the buttons to be drawn onto the screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def detect(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action

class Text():#Creates the Text class
    def __init__(self, screen):
        self.screen = screen

    def draw_text(self, text, font, text_col, x, y):#Allows the text to be drawn on the screen
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def draw_centered_text(self, text, font, text_col, screen_width, screen_height):
        img = font.render(text, True, text_col)
        x = screen_width // 2 - img.get_width() // 2
        y = screen_height // 2 - img.get_height() // 2
        self.screen.blit(img, (x, y))

class Player():
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.start_x = x
        self.start_y = y
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.lives = 5
        self.on_ground = False #checks if player is on the ground
    
    def update(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0
            if self.die():
                return True
        return False

    def die(self):
        self.lives -= 1
        self.respawn()
        return True
    
    def draw(self):
        screen.blit(self.image,(self.rect.x, self.rect.y))
        
    def check_collision(self, platforms, enemies):
        self.on_ground = False #resets every time this function takes place
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0: # falling down
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True #player is on solid ground
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.lives -= 1
                self.respawn()
                return True
        return False
                
    def respawn(self):
        self.rect.topleft = (self.start_x, self.start_y)
        self.vel_y = 0
                
class Platform():
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def draw_platform(self):
        screen.blit(self.image,(self.rect.x, self.rect.y))

class Coin():
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw_coin(self):
        screen.blit(self.image,(self.rect.x, self.rect.y))
    def check(self,player):
        if self.rect.colliderect(player.rect):
            database.insert_coins(150)
            return True
        return False

class Bullet:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.x += self.speed  # Moves to the right

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))  # Draws the bullet

    def check_collision(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                return enemy
        return None


class Weapon():
    def __init__(self, image, player, bullet_image):
        self.image = image
        self.player = player
        self.bullet_image = bullet_image
        self.last_shot = 0
        self.cooldown = 20
        self.rect = self.image.get_rect()
        self.rect.topleft = (170, 125)
        self.initial_position_set = False
        
    def draw(self, screen):
        if not self.initial_position_set:
            self.rect.topleft = (170, 125)
            self.initial_position_set = True
        else:
            self.rect.centerx = self.player.rect.centerx + 60
            self.rect.y = self.player.rect.top + 20
        screen.blit(self.image, self.rect.topleft)
        
    def shoot(self, current_frame, bullet_image):
        if current_frame - self.last_shot >= self.cooldown:
            bullet = Bullet(self.bullet_image, self.player.rect.centerx + 60, self.player.rect.centery - 5)
            self.last_shot = current_frame
            return bullet
        return None

class StartWeapon(Weapon):
    def __init__(self, image, player, bullet_image):
        super().__init__(image, player, bullet_image)
        self.name = "Start"

class RelicWeapon(Weapon):
    def __init__(self, image, player, bullet_image):
        super().__init__(image, player, bullet_image)
        self.cooldown = 15
        self.name = "Relic"

    def shoot(self, current_frame, bullet_image):
        if current_frame - self.last_shot >= self.cooldown:
            bullet = Bullet(self.bullet_image, self.player.rect.centerx + 60, self.player.rect.centery - 5)
            bullet.piercing = True  # Ensure the Bullet class supports this
            self.last_shot = current_frame
            return bullet
        return None


class Enemy():
    def __init__(self, image, x, y, speed):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.vel_y = 0
        self.on_platform = False
        
    def update(self,player,platforms):
        if not self.on_platform:
            self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        #calculate direction torwards player
        direction_x = player.rect.centerx - self.rect.centerx
        if direction_x != 0:
            direction_x = direction_x // abs(direction_x)
        #move torwards player
        self.rect.x += direction_x * self.speed
        self.on_platform = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_platform = True
        # Check if the player is at a higher position or there's no platform in front
        if not any(platform.rect.collidepoint(self.rect.centerx + direction_x * self.speed, self.rect.bottom + 1) for platform in platforms):
            if self.on_platform and self.vel_y == 0: # Jump only if on platform and not already jumping/falling
                self.vel_y = -10 # Jump velocity
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.speed = -self.speed
        if self.rect.top > SCREEN_HEIGHT:
            return False
        return True
    
    def draw (self,screen):
        screen.blit(self.image, self.rect.topleft)

class FinishLine():
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        
    def check(self, player):
        return self.rect.colliderect(player.rect)
