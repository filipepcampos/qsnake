import pygame
import numpy as np
from player import Player
from screen import Screen
from food import Food

WIDTH = 30
HEIGHT = 30
PX_SIZE = 20
MAP = "map.csv"
FPS = 20

# ACTIONS : [UP, DOWN, LEFT, RIGHT]   [0, 1, 2, 3]

def main():
    screen = Screen(WIDTH, HEIGHT, PX_SIZE, MAP)
    player = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
    food = Food(WIDTH, HEIGHT, screen.grid)   
    mainloop = True
    clock = pygame.time.Clock()

    while mainloop:
        clock.tick(FPS)
        screen.blit(player.pos, food.pos, player.tail) 

        action = register_keypress()
        player.change_action(action)
        player.move()
        player.check_food(food)
        mainloop = player.check_death()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False

def register_keypress():
    ''' Register keypresses
    
    Returns:
        action (int): number from [0, 1, 2, 3] that represents next action to take 
    '''
    keys = pygame.key.get_pressed()
    action = None
    if keys[pygame.K_UP]:
        action = 0
    elif keys[pygame.K_DOWN]:
        action = 1
    elif keys[pygame.K_LEFT]:
        action = 2
    elif keys[pygame.K_RIGHT]:
        action = 3
    return action

if __name__ == "__main__":
    main() 