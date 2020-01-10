import pygame
import numpy as np
from player import Player
from screen import Screen
from food import Food
from keypress import *

WIDTH = 30
HEIGHT = 30
PX_SIZE = 20
FPS = 20

def main():        
    pygame.display.set_caption("QSnake")    
    icon = pygame.image.load("./assets/icon.png")
    pygame.display.set_icon(icon)
    game()
    pygame.quit()

def game():
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

            if register_quit(): 
                return False
            if register_esc():
                return True
            
        
        player.clean_tail()
        screen.draw_winner(winner="gameover")
        mainloop, quit_game = wait_continue(mainloop, quit_game)
        if quit_game:
            return False
    return True

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