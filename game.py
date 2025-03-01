# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 15:19:25 2018

@author: zou
"""
import pygame, random
import numpy as np

class Settings:
    def __init__(self):
        self.width = 28
        self.height = 28
        self.rect_len = 15

class Snake:
    def __init__(self):
        #attributes for magic helmet
        self.multiplier = 1
        self.speed_added = 0

        self.death = 'CRASHED'
        
        self.image_up = pygame.image.load('images/snake_head_up.png')
        self.image_down = pygame.image.load('images/snake_head_down.png')
        self.image_left = pygame.image.load('images/snake_head_left_side.png')
        self.image_right = pygame.image.load('images/snake_head_right_side.png')

        self.tail_up = pygame.image.load('images/tail_up.png')
        self.tail_down = pygame.image.load('images/tail_down.png')
        self.tail_left = pygame.image.load('images/tail_left.png')
        self.tail_right = pygame.image.load('images/tail_right.png')
            
        self.image_body = pygame.image.load('images/body.png')

        self.facing = "right"
        self.initialize()

    def initialize(self):
        self.position = [6, 6]
        self.facing = "right"
        self.segments = [[6 - i, 6] for i in range(3)]
        #makes sure the snake doesn't have a helmet
        self.remove_helmet()

        self.score = 0
        #sets default death message to CRASHED
        self.death = 'CRASHED'
        self.helmet_duration = -1
        self.speed_added = 0

    def blit_body(self, x, y, screen):
        screen.blit(self.image_body, (x, y))
        
    def blit_head(self, x, y, screen):
        if self.facing == "up":
            screen.blit(self.image_up, (x, y))
        elif self.facing == "down":
            screen.blit(self.image_down, (x, y))  
        elif self.facing == "left":
            screen.blit(self.image_left, (x, y))  
        else:
            screen.blit(self.image_right, (x, y))  
            
    def blit_tail(self, x, y, screen):
        tail_direction = [self.segments[-2][i] - self.segments[-1][i] for i in range(2)]
        
        if tail_direction == [0, -1]:
            screen.blit(self.tail_up, (x, y))
        elif tail_direction == [0, 1]:
            screen.blit(self.tail_down, (x, y))  
        elif tail_direction == [-1, 0]:
            screen.blit(self.tail_left, (x, y))  
        else:
            screen.blit(self.tail_right, (x, y))  
    
    def blit(self, rect_len, screen):
        self.blit_head(self.segments[0][0]*rect_len, self.segments[0][1]*rect_len, screen)                
        for position in self.segments[1:-1]:
            self.blit_body(position[0]*rect_len, position[1]*rect_len, screen)
        self.blit_tail(self.segments[-1][0]*rect_len, self.segments[-1][1]*rect_len, screen)                
            
    
    def update(self):
        if self.facing == 'right':
            self.position[0] += 1
        if self.facing == 'left':
            self.position[0] -= 1
        if self.facing == 'up':
            self.position[1] -= 1
        if self.facing == 'down':
            self.position[1] += 1
        self.segments.insert(0, list(self.position))

    #Adds magic helmet which changes the snakes appearance
    #doubles points and increases speed.
    def add_helmet(self):
        
        #doubles point multiplier
        self.multiplier = 2
        #adds 10 more frames per second.
        self.speed_added = 10

        #changes sprite images
        self.image_up = pygame.image.load('images/snake_head_up_helmet.png')
        self.image_down = pygame.image.load('images/snake_head_down_helmet.png')
        self.image_left = pygame.image.load('images/snake_head_left_side_helmet.png')
        self.image_right = pygame.image.load('images/snake_head_right_side_helmet.png')

        #changes attribute to 8 seconds in the future to record duration.
        self.helmet_duration = pygame.time.get_ticks() + 8000
        
    #removes helmet from snake, calls this when duration reached.
    def remove_helmet(self):

        #falls back to default values
        self.multiplier = 1
        self.speed_added = 0

        #changes sprites back to default
        self.image_up = pygame.image.load('images/snake_head_up.png')
        self.image_down = pygame.image.load('images/snake_head_down.png')
        self.image_left = pygame.image.load('images/snake_head_left_side.png')
        self.image_right = pygame.image.load('images/snake_head_right_side.png')


        
class Strawberry():
    def __init__(self, settings):
        self.settings = settings
        
        #chooses the first 7 fruits.
        self.style = str(random.randint(1, 7))
        self.image = pygame.image.load('images/food' + str(self.style) + '.png')    

        self.change_time = 0

        self.initialize()
        
    def random_pos(self, snake):

        self.change_time = 0

        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.png')           
        
        self.position[0] = random.randint(0, self.settings.width-1)
        self.position[1] = random.randint(0, self.settings.height-1)

        self.position[0] = random.randint(9, 19)
        self.position[1] = random.randint(9, 19)
        
        if self.position in snake.segments:
            self.random_pos(snake)

        #records the current time + 3 seconds to check for duration of green apple
        elif self.style == '8':
            self.change_time = pygame.time.get_ticks() + 3000
            

    def blit(self, screen):
        screen.blit(self.image, [p * self.settings.rect_len for p in self.position])
   
    def initialize(self):
        self.position = [15, 10]
      
        
class Game:

    def __init__(self):
        self.settings = Settings()
        self.snake = Snake()
        self.strawberry = Strawberry(self.settings)
        self.move_dict = {0 : 'up',
                          1 : 'down',
                          2 : 'left',
                          3 : 'right'}       
        pygame.init()
        #plays munch sound effect
        self.munch_sound = pygame.mixer.Sound('./sound/munch-sound-effect.mp3')
        
    def restart_game(self):
        self.snake.initialize()
        self.strawberry.initialize()

    def current_state(self):         
        state = np.zeros((self.settings.width+2, self.settings.height+2, 2))
        expand = [[0, 1], [0, -1], [-1, 0], [1, 0], [0, 2], [0, -2], [-2, 0], [2, 0]]
        
        for position in self.snake.segments:
            state[position[1], position[0], 0] = 1
        
        state[:, :, 1] = -0.5        

        state[self.strawberry.position[1], self.strawberry.position[0], 1] = 0.5
        for d in expand:
            state[self.strawberry.position[1]+d[0], self.strawberry.position[0]+d[1], 1] = 0.5
        return state
    
    def direction_to_int(self, direction):
        direction_dict = {value : key for key,value in self.move_dict.items()}
        return direction_dict[direction]
        
    def do_move(self, move):
        move_dict = self.move_dict
        change_direction = move_dict[move]
        
        if change_direction == 'right' and not self.snake.facing == 'left':
            self.snake.facing = change_direction
        if change_direction == 'left' and not self.snake.facing == 'right':
            self.snake.facing = change_direction
        if change_direction == 'up' and not self.snake.facing == 'down':
            self.snake.facing = change_direction
        if change_direction == 'down' and not self.snake.facing == 'up':
            self.snake.facing = change_direction

        self.snake.update()
        
        if self.snake.position == self.strawberry.position:
            #if the strawberry is not a green apple
            if self.strawberry.style != '8':
                pygame.mixer.Sound.play(self.munch_sound)
                #added one point for first 4 fruits
                if int(self.strawberry.style) < 5:
                    self.snake.score += 1 * self.snake.multiplier
                #added two points for next 2 fruits
                elif int(self.strawberry.style) < 7:
                    self.snake.score += 2 * self.snake.multiplier
                #added three points for next fruit
                elif self.strawberry.style == '7':
                    self.snake.score += 3 * self.snake.multiplier
                    

                self.strawberry.random_pos(self.snake)
                reward = 1
                #calls add_helmet if the score is a direct multiple of 10
                if self.snake.score % 10 == 0:
                    self.snake.add_helmet()
                

        else:
            self.snake.segments.pop()
            reward = 0
                
        if self.game_end():
            return -1

        #if the fruit is a green apple
        if self.strawberry.style == '8':
            #if the duration of the green apple is up, it turns into a new fruit.
            if pygame.time.get_ticks() > self.strawberry.change_time:
                self.strawberry.random_pos(self.snake)

        #if the magic helmet is finished, remove helmet
        if self.snake.helmet_duration < pygame.time.get_ticks():
            self.snake.remove_helmet()
        return reward
    
    def game_end(self):
        end = False
        if self.snake.position[0] >= self.settings.width or self.snake.position[0] < 0:
            end = True
        if self.snake.position[1] >= self.settings.height or self.snake.position[1] < 0:
            end = True
        if self.snake.segments[0] in self.snake.segments[1:]:
            end = True
        #If the snake is on the green apple it will 
        # change its death message to "BAD APPLE"
        # and end the game
        if self.strawberry.style == '8' and self.snake.position == self.strawberry.position:
            self.snake.death = 'BAD APPLE'
            end = True

        return end
    
    def blit_score(self, color, screen):
        font = pygame.font.SysFont(None, 25)
        text = font.render('Score: ' + str(self.snake.score), True, color)
        screen.blit(text, (0, 0))

