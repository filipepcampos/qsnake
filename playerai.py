import pygame
import numpy as np
from player import Player
from screen import Screen
from food import Food
from get_state import get_state
import menu
from keypress import *

WIDTH = 30
HEIGHT = 30
PX_SIZE = 20
DATA = "./data/data13/"

fps = 20

def main():
    mainloop, quit_game = True, False
    q_table = np.load(DATA + "data.npy")
    clock = pygame.time.Clock()
    screen = Screen(WIDTH, HEIGHT, PX_SIZE, None, True)  

    while mainloop:
        # Restart game for another round
        player = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
        player_ai = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
        food = Food(WIDTH, HEIGHT, screen.grid)
        screen.blit(player, food, player_ai) 
        
        action, quit_game, mainloop = wait_start(mainloop, quit_game)

        player.change_action(action)
        player_ai.change_action(0)
        state = get_state(player_ai, food, WIDTH, HEIGHT)
        loop = True

        while mainloop and loop:
            clock.tick(fps)
            state = get_state(player_ai, food, WIDTH, HEIGHT)
            # Move player_ai and update time
            action = np.argmax(q_table[state]) 
            player_ai.change_action(action)
            player_ai.move()

            # Move player
            action = register_keypress(player.direction)
            player.change_action(action)
            player.move()

            # Check conditions            
            player.check_food(food)
            player_ai.check_food(food)
            player_ai_death, player_death = player_ai.check_death(player.pos), player.check_death(player_ai.pos)
            loop = player_ai_death and player_death
            if not player_ai_death or not player_death:
                print_winner(player, player_ai, player_death, player_ai_death)
            
            # Update the screen
            if loop or (not player_ai_death and not player_death):
                screen.blit(player, food, player_ai)
            
            mainloop = not register_esc()
            quit_game = register_quit()
            if quit_game:
                mainloop = False
        
        player.clean_tail()
        player_ai.clean_tail()
        screen.draw_alpha(winner="player1")
        mainloop, quit_game = wait_continue(mainloop, quit_game)        
    menu.main(not quit_game)

def wait_start(mainloop, quit_game):
    ''' Wait for input at the start of the game '''
    action = None
    while action == None and mainloop == True:            
        action = register_keypress()
        quit_game = register_quit()
        mainloop = not register_esc()
        if quit_game:
            mainloop = False
    return action, quit_game, mainloop

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

def print_winner(player, player_ai, player_death, player_ai_death):
    #! Change to correct scoring
    if not player_ai_death and not player_death:
        print("Tie")
    elif not player_death:
        print("AI wins")
    elif not player_ai_death:
        print("Player wins")

if __name__ == "__main__":
    main() 