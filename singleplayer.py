import pygame
import numpy as np
from player import Player
from screen import Screen
from food import Food
import menu
from keypress import *

WIDTH = 30
HEIGHT = 30
PX_SIZE = 20
MAP = "map.csv"
FPS = 20

def main():
    screen = Screen(WIDTH, HEIGHT, PX_SIZE, MAP) 
    mainloop, loop, quit_game = True, True, False
    clock = pygame.time.Clock()

    while mainloop:
        player = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
        food = Food(WIDTH, HEIGHT, screen.grid)  
        screen.blit(player.pos, food.pos, player.tail, player.score)
        loop = True
        while loop:
            clock.tick(FPS)
            screen.blit(player.pos, food.pos, player.tail, player.score) 

            action = register_keypress()
            player.change_action(action)
            player.move()
            player.check_food(food)
            loop = player.check_death()

            quit_game = not register_quit()
            if quit_game: 
                mainloop = False
                loop = False
        
        player.clean_tail()
        mainloop = wait_continue(mainloop)
    menu.main(quit_game)

def wait_continue(mainloop):
    ''' Wait and for continue input '''
    continue_game = False
    while not continue_game and mainloop:
        mainloop = register_quit()
        continue_game = register_enter()
    return mainloop


if __name__ == "__main__":
    main() 