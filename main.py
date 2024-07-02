import random
import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite): #Sprite
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('Graphics/Player/walk1.png').convert_alpha()
        player_walk2 = pygame.image.load('Graphics/Player/walk2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.index = 0  # pick btw walk1/walk2
        self.player_jump = pygame.image.load('Graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound  = pygame.mixer.Sound('Audio/Jump.mp3') #import sound
        self.jump_sound.set_volume(0.25) #btw 0-1
    def player_input(self):
        keys = pygame.key.get_pressed() #store all key pressed
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300: #when space pressed and player on ground
            self.gravity = -20 #jump
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1#gradually increase gravity
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom =300 #keep player on ground

    def animation(self):
        if self.rect.bottom <300:
            self.image = self.player_jump #jump img
        else:
            self.index +=0.1 #change from 0 to 1 slowly
            if self.index >= len(self.player_walk) : self.index = 0
            self.image = self.player_walk[int(self.index)] #walk animation

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):#type of obstacle
        super().__init__()

        if type == 'fly':
            fly1 = pygame.image.load('Graphics/Fly1.png').convert_alpha()# removes alpha values in image/ makes it like png
            fly2 = pygame.image.load('Graphics/Fly2.png').convert_alpha()
            self.frames = [fly1, fly2]
            y_pos = 200
        else:
            snail1 = pygame.image.load('Graphics/snail1.png').convert_alpha()
            snail2 = pygame.image.load('Graphics/snail2.png').convert_alpha()
            self.frames = [snail1, snail2]
            y_pos = 300

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900,1100), y_pos)) 

    def animation(self):
        self.index += 0.1
        if self.index > len(self.frames): self.index = 0 #if index > 2, index = 0
        self.image = self.frames[int(self.index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill() #destroys obstacle sprite if ouside screen

    def update(self):
        self.animation()
        self.rect.x -= 5
        self.destroy()
def display_score():
    current_time = int(pygame.time.get_ticks()/1000)- start_time#time in seconds
    score_surface = font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface, score_rect)
    return  current_time
def display_lives(lives):
    heart_w, heart_h = 30, 30 #desired heart size
    heart = pygame.transform.scale(heart_surface, (heart_w, heart_h)) #scaled heart image
    for i in range(lives):
        screen.blit(heart, (680+i *(heart_w+10), 10))

# def obstacle_movement(obstacle_list):
#     if obstacle_list: #if list not empty
#         for obstacle_rect in obstacle_list:
#             obstacle_rect.x -= 5 #moves every obstacle_rect to left by 5
#             if obstacle_rect.bottom == 300: screen.blit(snail_surface, obstacle_rect)
#             else: screen.blit(fly_surface, obstacle_rect)
#         #remove any rect that is outside screen
#         obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x >-100] #copy item from og list if its on screen
#         return  obstacle_list
#     else: return [] #return empty list

# def collision(player, obstacles):
#     if obstacles: #if obstacles list is not empty
#         for obstacle_rect in obstacles:
#             if player.colliderect(obstacle_rect):
#                 return False #running = False
#     return True #running = True

def collision_sprite():
    global lives
    if pygame.sprite.spritecollide(player.sprite,obstacle_group, True): #True = deletes obstacle after collision
        lives -=1
        life_sound.play() #sound effect when life lost
        if lives <=0:
            obstacle_group.empty() #delete all sprites after collision/ for retry game
            return True #collision = True
    else:
        return False
# Variables
pygame.init() #starts src and initializes all its sub parts
width , height =800, 400
screen = pygame.display.set_mode((width, height)) # display surface
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
font = pygame.font.Font('Font/Pixeltype.ttf', 50)
running = False
player_gravity = 0
start_time = 0
score = 0
lives = 3
bg_music =pygame.mixer.Sound('Audio/Music.wav')
bg_music.set_volume(0.063)
bg_music.play()
life_sound = pygame.mixer.Sound('Audio/LifeLost.wav')
life_sound.set_volume(0.5)

# Groups
player  = pygame.sprite.GroupSingle() #player is a group, containing Player() sprite
player.add(Player()) #add player object into GroupSingle
obstacle_group = pygame.sprite.Group()#instead of adding obstacles to group here, add em when obstacle_timer ticks

#Images
sky_surface = pygame.image.load('Graphics/sky.png').convert() #using convert() makes game run faster
ground_surface = pygame.image.load('Graphics/ground.png').convert()
heart_surface = pygame.image.load('Graphics/heart.png').convert_alpha()

#Intro screen
player_stand = pygame.image.load('Graphics/Player/stand.png').convert_alpha()
player_stand= pygame.transform.rotozoom(player_stand, 0, 2) #img, rotate angle, 2x scale
player_stand_rect = player_stand.get_rect(center = (400,200)) #place player at center

game_name = font.render('Pixel Runner', False, (111,196, 169))
game_name_rect = game_name.get_rect(center = (400,50))

instructions = font.render('Press Space to start game', False, (111,196, 169))
instructions_rect = instructions.get_rect(center = (400, 350))

# Timers
obstacle_timer = pygame.USEREVENT + 1 #add +1 for custom user events as src alr has its own events
pygame.time.set_timer(obstacle_timer, 1500) #event, interval in ms

while True: #screen visible forever until False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if X pressed
            pygame.quit()
            exit() #closes while loop too
        if running:
            if event.type == obstacle_timer: #if custom event is triggered
                # add obstacles to list with diff starting pos:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail']))) #randomly chooses from options

        else: #RESTART
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:#when space pressed after game ends
                    running = True
                    start_time = int(pygame.time.get_ticks()/1000) #update start_time to current time
                    lives = 3
                    bg_music.play(loops = -1) #resume music

    if running:
        screen.blit(sky_surface, (0,0)) #used to put a surface on another surface
        screen.blit(ground_surface, (0,300))
        score = display_score()
        display_lives(lives) #display hearts

        # Player
        player.draw(screen) #draw player groupSingle on screen
        player.update() #calls all methods inside it - updates player

        obstacle_group.draw(screen)
        obstacle_group.update() #calls all methods inside

        # Collision
        running = not(collision_sprite()) #running False when collision True

    else:

        screen.fill((94, 129, 162))
        screen.blit(game_name, game_name_rect)
        screen.blit(player_stand, player_stand_rect)

        score_msg = font.render(f'Your score: {score}', False, (111, 196, 169))
        score_msg_rect = score_msg.get_rect(center=(400, 350))

        if score == 0: screen.blit(instructions, instructions_rect)
        else: screen.blit(score_msg, score_msg_rect)
        bg_music.stop()  # stop music
    pygame.display.update() #keeps updating display surface
    clock.tick(60) #makes While loop run within 60 times/second == 60fps






 # keys = src.key.get_pressed() #tuple- returns 1/0 for any key pressed
    # if keys[src.K_SPACE]: #returns 1 if space is pressed
    #     print('Jump')

    # if player_rect.colliderect(snail_rect): #returns 0 / 1
    #     print  ('collision')

    # mouse_position = src.mouse.get_pos() #get x , y position of mouse
    # if player_rect.collidepoint((mouse_position)):
    #     print(src.mouse.get_pressed())