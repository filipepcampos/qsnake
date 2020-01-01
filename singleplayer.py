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
FPS = 20

def main():
    screen = Screen(WIDTH, HEIGHT, PX_SIZE, None) 
    mainloop, quit_game = True, False
    clock = pygame.time.Clock()

    while mainloop:
        player = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
        food = Food(WIDTH, HEIGHT, screen.grid)  
        screen.blit(player, food)
        loop = True
        while mainloop and loop:
            clock.tick(FPS)
            screen.blit(player, food) 

            action = register_keypress()
            player.change_action(action)
            player.move()
            player.check_food(food)
            loop = player.check_death()

            quit_game = register_quit()
            mainloop = not register_esc()
            if quit_game: 
                mainloop = False
        
        player.clean_tail()
        mainloop, quit_game = wait_continue(mainloop, quit_game)
    menu.menu(not quit_game)

def wait_continue(mainloop, quit_game):
    ''' Wait for input at the end of the game '''
    continue_game = False
    while not continue_game and mainloop:
        mainloop = not register_esc()
        continue_game = register_enter()
        quit_game = register_quit()
        if quit_game:
            mainloop = False
    return mainloop, quit_game


if __name__ == "__main__":
    main() 