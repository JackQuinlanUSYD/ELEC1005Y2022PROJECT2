# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""

from cmath import rect
from tkinter import CENTER
import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT

from game import Game

#colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
gold = pygame.Color(255, 191, 0)
red = pygame.Color(255, 90, 0)
pink = pygame.Color(255, 16, 240)
yellow = pygame.Color(255, 191, 0)
lBrown = pygame.Color(106, 78, 66)
brown = pygame.Color(90, 62, 50)
dBrown = pygame.Color(50, 26, 24)
lBrown1 = pygame.Color(195, 155, 119)

#background image
background = pygame.image.load('images/background.jpg')

#fruit graphics for pg2 instructions
bananaF = pygame.image.load('images/food1.bmp')
eggPF = pygame.image.load('images/food2.bmp')
gAppleF = pygame.image.load('images/food3.bmp')
gAppleF1 = pygame.transform.scale(gAppleF, (40, 40)) 
kiwiF = pygame.image.load('images/food4.bmp')
lemonF = pygame.image.load('images/food5.bmp')
mangoF = pygame.image.load('images/food6.bmp')
orangeF = pygame.image.load('images/food7.bmp')
peachF = pygame.image.load('images/food8.bmp')

#initial interface graphics
start_img_off = pygame.image.load('images/start_btn.png')
start_img = pygame.image.load('images/start_btnOn.png')
exit_img_off = pygame.image.load('images/exit_btn.png')
exit_img = pygame.image.load('images/exit_btnOn.png')
scroll_clsd_off = pygame.image.load('images/test1scroll_ac.png')
scroll_clsd = pygame.image.load('images/test1scroll.png')
scroll_opnd = pygame.image.load('images/scroll_opnd1.png')

#starts the game
game = Game()
rect_len = game.settings.rect_len
#makes the snake
snake = game.snake
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((game.settings.width  * 15, 
                                  game.settings.height * 15))
pygame.display.set_caption('Gluttony')

#crash and background sounds and images 
crash_img = pygame.image.load("images/splat.bmp")
crash_img = pygame.transform.scale(crash_img, (400,400))
crash_sound = pygame.mixer.Sound('./sound/crash.wav')
background_music = pygame.mixer.Sound('./sound/candy.wav')

#new title images
title_font = pygame.font.Font("images/Fonts/Wicked_Mouse.ttf", 35)
instruct_font = pygame.font.Font('images/Fonts/Minecraft.ttf', 14)
instruct_top_font = pygame.font.Font('images/Fonts/Minecraft.ttf', 20)
num_font = pygame.font.Font('images/Fonts/Minecraft.ttf', 28)

#starting title
starting_message_back = title_font.render("Gluttonous", True, black)
starting_message = title_font.render("Gluttonous", True, yellow)

#pg1 instruction messages, split into each line.
instruct_msg = instruct_font.render("Navigate around the", True, lBrown)
instruct_msg1 = instruct_font.render("screen with", True, lBrown)
instruct_msg2 = instruct_font.render("arrow keys.", True, lBrown)

instruct_msg3 = instruct_font.render("Eat as many fruits", True, lBrown)
instruct_msg4 = instruct_font.render("as possible and", True, lBrown)
instruct_msg5 = instruct_font.render("avoid crashing.", True, lBrown)

def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def message_display(text, x, y, color=black):
    large_text = pygame.font.Font("images/Fonts/Wicked_Mouse.ttf", 35)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()

def button(msg, x, y, w, h, inactive_img, active_img, action=None, parameter=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y: #checks if the current mouse coordinates collide with the buttons coordinates
        screen.blit(active_img, (x, y) )
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter)
            else:
                action()
    else:
        screen.blit(inactive_img, (x, y))

    smallText = pygame.font.SysFont('comicsansms', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)

def quitgame():
    pygame.quit()
    quit()
    
#Called when the snake loses, Takes death message as parameter and outputs death message and ends round
def crash(death): #
    #stops the music     
    pygame.mixer.stop()
    #plays crash sound
    pygame.mixer.Sound.play(crash_sound)
    #displays crash message alternating colours 3 times
    for messages in range(3):
        message_display(death, game.settings.width /2 * 15 + 3, game.settings.height /2 *15 - 20)
        message_display(death, game.settings.width / 2 * 15, game.settings.height / 3 * 20, gold)
        time.sleep(0.05)
        message_display(death, game.settings.width /2 * 15 + 3, game.settings.height /2 *15 - 20, gold)
        message_display(death, game.settings.width / 2 * 15, game.settings.height / 3 * 20, red)
        time.sleep(0.05)
    #displays crash message in the same colour for 2 seconds
    message_display(death, game.settings.width /2 * 15 + 3, game.settings.height /2 *15 - 20)
    message_display(death, game.settings.width / 2 * 15, game.settings.height / 3 * 20, gold)
    time.sleep(2)

        
def initial_interface(): #menu
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT or intro == False:
                quitgame()
                
        screen.fill(white) #starting screen display
        screen.blit(background, (0, 0))

        screen.blit(starting_message_back,
                   (game.settings.width / 5.9 * 15, 
                    game.settings.height / 4.6 * 15))

        screen.blit(starting_message,  
                   (game.settings.width / 6.2 * 15, 
                    game.settings.height / 4.7 * 15)) 

        button('', 80, 185, 100, 45, 
               start_img_off, start_img, 
               game_loop, 'human') 

        button('', 240, 185, 100, 45, 
               exit_img_off, exit_img, 
               quitgame) #exit button

        button('', 165, 280, 90, 35, 
               scroll_clsd_off, scroll_clsd, 
               instruct_screen, 1)

        pygame.display.update()
        pygame.time.Clock().tick(1500)

def game_loop(player, fps=10): #Plays the game
    game.restart_game()

    #play background music when the game starts
    pygame.mixer.Sound.play(background_music, -1)

    fps = 5
    prev_score = 0
    while not game.game_end():

        pygame.event.pump()

        move = human_move()
        #If the score has changed by 3 points or more the fps increases
        if (game.snake.score - prev_score >= 3) and (fps < 40):
            prev_score = game.snake.score
            fps += 1
        
        #uses increased multiplier to check if to show MAGIC HELMET message
        if game.snake.multiplier == 2:
            message_display('MAGIC HELMET', game.settings.width / 2 * 15 + 3, game.settings.height - 3)
            message_display('MAGIC HELMET', game.settings.width / 2 * 15, game.settings.height, gold)
            
        game.do_move(move)

        screen.fill(black)
        screen.blit(background, (0, 0)) #displaying the background during game

        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)

        #uses increased multiplier to check if to show MAGIC HELMET message (repeated for faster flashing)
        if game.snake.multiplier == 2:
            message_display('MAGIC HELMET', game.settings.width / 2 * 15 + 3, game.settings.height - 3)
            message_display('MAGIC HELMET', game.settings.width / 2 * 15, game.settings.height, gold)

        pygame.display.flip()

        #runs off the fps accounting for the magic helmet speed increase
        fpsClock.tick(fps + game.snake.speed_added)

    crash(game.snake.death)

# the instruct_screen method takes in a int which refers to the page number
# and using the given button method, it will go to the related branch and display
# the relevant instruction page.
def instruct_screen(page):
    instruct = True
    while instruct:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        if page == 1:

            screen.fill(white)
            screen.blit(background, (0, 0))

            screen.blit(scroll_opnd,   (85 , 42))
            screen.blit(instruct_top_font.render("How to play",
                                                 True, 
                                                 brown), 
                                                 (155, 61))

            instruct_msg_ls = [[instruct_msg,  142, 109],
                               [instruct_msg1, 170, 129],
                               [instruct_msg2, 170, 149],
                               [instruct_msg3, 148, 185],
                               [instruct_msg4, 157, 205],
                               [instruct_msg5, 157, 225]]

            for i in range(len(instruct_msg_ls)):
                for j in range(len(instruct_msg_ls[i])):
                    j = 0
                    screen.blit(instruct_msg_ls[i][j], 
                               (instruct_msg_ls[i][j + 1], 
                                instruct_msg_ls[i][j + 2]))
            # the for loops above iterates through the 2D instruction list, which contains the msg and their coordinates
            # and blits the messages.

            button('', 160, 360, 100, 50, 
                   exit_img_off, exit_img, 
                   initial_interface)
            
            num_x = 171
            for i in range (3):
                if i + 1 == page:
                    button('', num_x, 315, 20, 20, 
                           num_font.render(str(i + 1), True, lBrown1), 
                           num_font.render(str(i + 1), True, lBrown1))
                else:
                    button('', num_x, 315, 20, 20, 
                           num_font.render(str(i + 1), True, dBrown), 
                           num_font.render(str(i + 1), True, lBrown1), 
                           instruct_screen, i + 1)     
                num_x+=30  
        
        if page == 2 :
            fruits1 = [kiwiF, orangeF, bananaF]
            fruit1_y = 107
            
            fruits2 = [eggPF, lemonF, peachF]
            fruit2_y = 166

            screen.fill(white)
            screen.blit(background, (0, 0))

            screen.blit(scroll_opnd, (85 , 42))
            screen.blit(instruct_top_font.render("Fruit Points", 
                                                 True, 
                                                 brown), 
                                                 (158, 61))

            for fruit1 in fruits1:
                screen.blit(fruit1, (176, fruit1_y))
                fruit1_y += 17

            screen.blit(instruct_font.render("~ 1 pts",
                                             True,
                                             brown), 
                                             (197, 126))

            for fruit2 in fruits2:
                screen.blit(fruit2, (176, fruit2_y))
                fruit2_y += 17

            screen.blit(instruct_font.render("~ 2 pts",
                                             True,
                                             brown), 
                                             (197, 185))
        
            screen.blit(mangoF, (176, 222))
            screen.blit(instruct_font.render("~ 3 pts",
                                             True,
                                             brown), 
                                             (197, 224))

            button('', 160, 360, 100, 50, 
                   exit_img_off, exit_img, 
                   initial_interface)

            num_x = 171
            for i in range (3):
                if i + 1 == page:
                    button('', num_x, 315, 20, 20, 
                           num_font.render(str(i + 1), True, lBrown1), 
                           num_font.render(str(i + 1), True, lBrown1))
                else:
                    button('', num_x, 315, 20, 20, 
                           num_font.render(str(i + 1), True, dBrown), 
                           num_font.render(str(i + 1), True, lBrown1), 
                           instruct_screen, i + 1)     
                num_x+=30       
        
        if page == 3:
            screen.fill(white)
            screen.blit(background, (0, 0))

            screen.blit(scroll_opnd,   (85 , 42))
            screen.blit(instruct_top_font.render("The Green Apple.", 
                                                 True,
                                                 brown), 
                                                 (130, 61))

            screen.blit(gAppleF1, (190, 110))
            
            screen.blit(instruct_font.render("avoid the", 
                                             True, 
                                             brown), 
                                             (179, 160))

            screen.blit(instruct_font.render("green apple at", 
                                             True, 
                                             brown), 
                                             (162, 180))
            screen.blit(instruct_font.render("all cost.", 
                                             True, 
                                             brown), 
                                             (185, 200))
            screen.blit(instruct_font.render("or face death", 
                                             True, 
                                             brown), 
                                             (162, 220))

            button('', 160, 360, 100, 50, 
                   exit_img_off, exit_img, 
                   initial_interface)

            num_x = 171
            for i in range (3):
                if i + 1 == page:
                    button('', num_x, 315, 20, 20, 
                           num_font.render(str(i + 1), True, lBrown1), 
                           num_font.render(str(i + 1), True, lBrown1))
                else:
                    button('', num_x, 315, 20, 20, 
                           num_font.render(str(i + 1), True, dBrown), 
                           num_font.render(str(i + 1), True, lBrown1), 
                           instruct_screen, i + 1)     
                num_x+=30  

        pygame.display.update()
        pygame.time.Clock().tick(15)
           

def human_move():
    direction = snake.facing #stores the current direction

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        elif event.type == KEYDOWN: #when any of the arrow keys are pressed, checks which one is pressed
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    move = game.direction_to_int(direction)
    return move


if __name__ == "__main__":
    initial_interface()
