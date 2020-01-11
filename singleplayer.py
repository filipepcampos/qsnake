import pygame
import numpy as np
from player import Player
from screen import Screen
from food import Food
from keypress import register_events, register_enter

WIDTH = 30
HEIGHT = 30
PX_SIZE = 20
FPS = 15

def main():
    pygame.init()        
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
        action = None
        food = Food(WIDTH, HEIGHT, screen.grid)  
        screen.blit(player, food)
        loop = True
        while mainloop and loop:
            clock.tick(FPS)
            screen.blit(player, food) 

            action, esc, quit_game = register_events(action)
            if esc:
                return True
            if quit_game:
                return False
            player.change_action(action)
            player.move()
            player.check_food(food)
            loop = player.check_death()
            
        
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
        _, esc, quit_game = register_events()
        mainloop = not esc
        continue_game = register_enter()
        if quit_game:
            mainloop = False
    return mainloop, quit_game


if __name__ == "__main__":
    main() 