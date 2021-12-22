import pygame
from utils import scale_img, resize_img
from random import *

# amount = int(input("how many ais would you like? "))
# print("Open the playing window,", " And Have Fun!")
amount = 1000
plyr_size = 30
WIN = pygame.display.set_mode((500, 500), 100)
pygame.display.set_caption("AI vs Player")
Player_img = resize_img(pygame.image.load("Player.img.png"), plyr_size)
Enemy_img = resize_img(pygame.image.load("Enemy2.img.png"), plyr_size)
background_img = scale_img(pygame.image.load("Level.img.png2.png"), 3)
background_mask = pygame.mask.from_surface(background_img)
start_img = resize_img(pygame.image.load("Start_Amount_Ais.png"), plyr_size)
IMG = Player_img
run = True
Ai_S_Pos = 2900
Plyr_S_Pos = (2700, 200)
scroll_x = 0
background_placement = ()
ai_and_player_info = []
repeat = 0
ai_count = 0
scroll_y = 0
PlayerX = 0
PlayerY = 0
plyr_y_vle = 0


class Player:
    # Importing all vars
    def __init__(self, jump_height, speed, is_player=-0, distance_player=0):
        self.img = IMG
        self.touching_ground = 0
        self.x_vel = 0
        self.y_vel = 0
        self.jump_height = jump_height
        self.speed = speed
        self.is_player = is_player
        self.distance_player = distance_player
        if is_player:
            self.x, self.y = Plyr_S_Pos
        else:
            self.x, self.y = Ai_S_Pos, randint(700, 1000)

    # Checking if this is the player or an AI
    def u_playing(self):
        global plyr_y_vle
        if self.is_player:
            self.y_vel = plyr_y_vle
        return self.is_player

    def move_x(self):
        self.x_vel = (self.x_vel * .9)
        self.x += self.x_vel

    def move_y(self):
        global plyr_y_vle
        self.y_vel += .3
        self.y += self.y_vel
        if self.is_player:
            plyr_y_vle = self.y_vel

    def key_pressed(self, right=False, left=False, up=False):
        global plyr_y_vle
        if self.is_player == 0:
            if self.x < PlayerX:
                self.x_vel += self.speed
            else:
                self.x_vel -= self.speed

            if self.y-10 > PlayerY and up:
                self.y_vel = self.jump_height
        else:
            if right:
                self.x_vel += self.speed
            elif left:
                self.x_vel -= self.speed
            elif up:
                self.y_vel = self.jump_height
                plyr_y_vle = self.y_vel

    def touching_player(self):
        if not self.is_player:
            self.distance_player = abs(((self.x - PlayerX)**2 + (self.y - PlayerY)**2)**.5)
            if self.distance_player < plyr_size:
                if self.y < PlayerY + (plyr_size/3):
                    return 2
                else:
                    return 1

    def collide(self, mask, x=0, y=0, y_off=0):
        player_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x + 100), int(self.y - y + 100 + y_off))
        poi = mask.overlap(player_mask, offset)
        return poi

    def collision(self, y=0, x=0, yup=0):
        global plyr_y_vle
        if yup != 0:
            self.y -= yup
            self.touching_ground = 1
        if y:
            self.y += (self.y_vel * -1)
            self.y_vel = 0
            self.touching_ground = 1
            if self.is_player:
                plyr_y_vle = self.y_vel
        if x:
            self.x += (self.x_vel * -1)
            self.x_vel = 0

    def draw(self, window):
        global scroll_x
        global scroll_y
        global PlayerX
        global PlayerY
        if self.is_player:
            scroll_x += ((self.x + scroll_x - 250) * -.1)
            scroll_y += ((self.y + scroll_y - 250) * -.1)
            PlayerX = self.x
            PlayerY = self.y
        if self.is_player:
            window.blit(Player_img, (self.x + scroll_x, self.y + scroll_y))
        else:
            window.blit(Enemy_img, (self.x + scroll_x, self.y + scroll_y))


def draw(win, enemy):
    win.blit(background_img, (-100 + scroll_x, -100 + scroll_y))
    for i in enemy:
        i.draw(win)
    pygame.display.update()


def add_ai():
    global repeat
    repeat = 0
    while repeat < amount:
        repeat += 1
        ai_and_player_info.append(Player((-1 * randint(1380, 1450)/100), randint(300, 500)/1000, 0))


def player_ded():
    global ai_and_player_info
    # Adding Player
    ai_and_player_info = [(Player(-18, .9, 1))]
    #     Adding AI(s)
    add_ai()


player_ded()

# Physics
while run:
    pygame.time.delay(10)
    keys = pygame.key.get_pressed()

    # Drawing everything
    WIN.fill((100, 100, 100))
    draw(WIN, ai_and_player_info)

    # AI and Player Physics
    ai_count = 0
    for a in ai_and_player_info:
        a.move_x()
        if a.collide(background_mask):
            a.collision(yup=1)
            if a.collide(background_mask):
                a.collision(yup=1)
                if a.collide(background_mask):
                    a.collision(yup=1)
                    if a.collide(background_mask):
                        a.collision(yup=1)
                        if a.collide(background_mask):
                            a.collision(yup=-4)
                            a.collision(x=1)

        # Move right and left
        if not a.u_playing():
            a.key_pressed()
        else:
            if keys[pygame.K_RIGHT]:
                a.key_pressed(right=True)

            if keys[pygame.K_LEFT]:
                a.key_pressed(left=True)

        a.move_y()

        if a.collide(background_mask):
            a.collision(y=1)

        # Jumping
        if a.collide(background_mask, y_off=1):
            if not a.u_playing():
                a.key_pressed(up=True)
            else:
                if keys[pygame.K_UP]:
                    a.key_pressed(up=True)

        if not a.u_playing():
            if a.touching_player() == 2:
                player_ded()
            elif a.touching_player() == 1:
                plyr_y_vle = -5
                ai_and_player_info.remove(ai_and_player_info[ai_count])
                if len(ai_and_player_info) < 2:
                    add_ai()
        ai_count += 1

    # This make it stop when you press exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

pygame.quit()
