import pygame
from game_object import GameObject
from player import Player
from enemy import Enemy
import random

class Game:
    def __init__(self):
        self.width = 750
        self.height = 950
        self.white_color = (255, 255, 255)
        self.game_window = pygame.display.set_mode((self.width, self.height))
        self.background = GameObject(0, 0, self.width, self.height, 'background1.png')
        self.cross = GameObject(330, 5, 50, 110, 'cross1.png')
        self.main_menu = GameObject(0, 0, self.width, self.height, 'main_menu.png')
        self.about_screen = GameObject(0, 0, self.width, self.height, 'about.png')
        self.clock = pygame.time.Clock()
        self.level = 1.0
        self.font = pygame.font.Font(None, 75)
        self.reset_map()
        self.state = "MENU"
        self.music_file = 'PIMEÄSAMMAKKO-Enochian_19_Avainta.mp3'
        self.music_status = False  
        self.sound_effects_status = False  
        self.enemy_collision_sound = pygame.mixer.Sound('ZombieMoan01.mp3')  
        self.cross_reached_sound = pygame.mixer.Sound('ZombieAttack05.mp3')  

    def control_music(self):
        if self.music_status:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play(-1)  
        else:
            pygame.mixer.music.stop()

    def get_level_text(self):
        text = str(int(self.level)) 
        color = (243, 36, 28) 
        return self.font.render(text, True, color) 

    def reset_map(self):
        player_speed = 1 + (self.level // 2) * 0.5
        self.player = Player(328, 850, 75, 100, 'corpse_mask15.png', player_speed)
        enemy_speed = 1 + (self.level * 0.5)
        self.enemies = []
        for _ in range(int(self.level)):
            x, y = self.get_random_position()
            self.enemies.append(Enemy(x, y, 50, 50, 'sun1.png', enemy_speed))

    def get_random_position(self):
        cross_padding = 50  
        player_padding = 50  
        enemy_width = 50 
        enemy_height = 50 
        while True:
            x = random.randint(0, self.width - enemy_width)
            y = random.randint(0, self.height - enemy_height)
            if self.cross.y + self.cross.height + cross_padding > y > self.cross.y - cross_padding - enemy_height:
                continue
            if self.player.y + player_padding > y > self.player.y - player_padding - enemy_height:
                continue
            return x, y

    def draw_objects(self):
        self.game_window.fill(self.white_color)
        self.game_window.blit(self.background.image, (self.background.x, self.background.y))
        self.game_window.blit(self.cross.image, (self.cross.x, self.cross.y))
        self.game_window.blit(self.player.image, (self.player.x, self.player.y))
        level_text = self.get_level_text() 
        self.game_window.blit(level_text, (10, 10)) 
        for enemy in self.enemies:
            self.game_window.blit(enemy.image, (enemy.x, enemy.y))
        pygame.display.update()

    def move_objects(self, player_direction):
        self.player.move(player_direction, self.height, self.width)  
        for enemy in self.enemies:
            enemy.move(self.width)


    def check_if_collided(self):
        for enemy in self.enemies:
            if self.detect_collisions(self.player, enemy):
                self.level = 1.0
                return True
        if self.detect_collisions(self.player, self.cross):
            self.level += 1.0
            return True
        return False

    def detect_collisions(self, object_1, object_2):
        if object_1.y > (object_2.y + object_2.height):
            return False
        elif (object_1.y + object_1.height) < object_2.y:
            return False
        if object_1.x > (object_2.x + object_2.width):
            return False
        elif (object_1.x + object_1.width) < object_2.x:
            return False
        return True

    def run_game_loop(self):
        while True:
            if self.state == "MENU":
                self.menu_loop()
            elif self.state == "ABOUT":
                self.about_loop()
            elif self.state == "GAME":
                self.game_loop()
            elif self.state == "PAUSED":
                self.pause_loop()

    def menu_loop(self):
        while self.state == "MENU":
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.state = "GAME"
                        self.reset_map()
                    elif event.key == pygame.K_2:
                        self.state = "ABOUT"
                    elif event.key == pygame.K_m:
                        self.music_status = not self.music_status
                        self.control_music()
                    elif event.key == pygame.K_s:
                        self.sound_effects_status = not self.sound_effects_status
                    elif event.key == pygame.K_3:
                        pygame.quit()
                        quit()

            self.game_window.blit(self.main_menu.image, (self.main_menu.x, self.main_menu.y))
            pygame.display.update()
            self.clock.tick(30)

    def about_loop(self):
        while self.state == "ABOUT":
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.music_status = not self.music_status
                        self.control_music()
                    elif event.key == pygame.K_s:
                        self.sound_effects_status = not self.sound_effects_status
                    else:
                        self.state = "MENU"
            self.game_window.blit(self.about_screen.image, (self.about_screen.x, self.about_screen.y))
            pygame.display.update()
            self.clock.tick(30)

    def game_loop(self):
        player_direction = [0, 0]  
        while self.state == "GAME":
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.state = "MENU"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player_direction[0] = -1
                    elif event.key == pygame.K_DOWN:
                        player_direction[0] = 1
                    elif event.key == pygame.K_LEFT:  
                        player_direction[1] = -1  
                    elif event.key == pygame.K_RIGHT:  
                        player_direction[1] = 1  
                    elif event.key == pygame.K_p:
                        self.state = "PAUSED"
                    elif event.key == pygame.K_q:
                        self.state = "MENU"
                    elif event.key == pygame.K_m:
                        self.music_status = not self.music_status
                        self.control_music()
                    elif event.key == pygame.K_s:
                        self.sound_effects_status = not self.sound_effects_status
                elif event.type == pygame.KEYUP:
                    if event.key in {pygame.K_UP, pygame.K_DOWN}:  
                        player_direction[0] = 0  
                    if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:  
                        player_direction[1] = 0  
            self.move_objects(player_direction)  
            self.draw_objects()
            if self.detect_collisions(self.player, self.cross):
                if self.sound_effects_status:  
                    self.cross_reached_sound.play()
                self.level += 1.0
                self.reset_map()   
            for enemy in self.enemies:
                if self.detect_collisions(self.player, enemy):
                    if self.sound_effects_status: 
                        self.enemy_collision_sound.play()  
                    self.level = 1.0
                    self.state = "MENU"
                    self.reset_map()
                    break
            self.clock.tick(80)

    def pause_loop(self):
        while self.state == "PAUSED":
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.state = "GAME"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.state = "GAME"
                    elif event.key == pygame.K_q:
                        self.state = "MENU"
                    elif event.key == pygame.K_m:
                        self.music_status = not self.music_status
                        self.control_music()
                    elif event.key == pygame.K_s:
                        self.sound_effects_status = not self.sound_effects_status
            self.draw_objects()  
            self.clock.tick(30)






