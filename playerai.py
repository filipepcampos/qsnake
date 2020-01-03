import pygame
import numpy as np
from player import Player
from screen import Screen
from food import Food
from get_state import get_state
from keypress import *

WIDTH = 30
HEIGHT = 30
PX_SIZE = 20
DATA = "./data/2/"

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
        if quit_game:
            return False

        player.change_action(action)
        player_ai.change_action(0)
        state = get_state(player_ai, food, WIDTH, HEIGHT)
        loop = True

        while mainloop and loop:
            clock.tick(fps)
            state = get_state(player_ai, food, WIDTH, HEIGHT)
            old_player_pos, old_player_ai_pos = player.pos, player_ai.pos
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
            player_ai_death, player_death = player_ai.check_death(player.pos, old_player_pos), player.check_death(player_ai.pos, old_player_ai_pos)
            swap = (player.pos == old_player_ai_pos and player_ai.pos == old_player_pos)
            if swap:
                player_death, player_ai_death = False, False
            loop = player_ai_death and player_death
            
            
            # Update the screen
            if loop: 
                screen.blit(player, food, player_ai)
            if player.pos == player_ai.pos:
                screen.blit(player, food, player_ai, collision="col")
            elif swap:
                screen.blit(player, food, player_ai, collision="col", collision2="col")

            if not loop:
                winner = get_winner(player, player_ai, player_death, player_ai_death)
                screen.draw_winner(winner=winner)

            mainloop = not register_esc()
            quit_game = register_quit()
            if quit_game:
                return False
        
        player.clean_tail()
        player_ai.clean_tail()
        mainloop, quit_game = wait_continue(mainloop, quit_game)        
        if quit_game:
            return False
    return True

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

def get_winner(player, player_ai, player_death, player_ai_death):
    ''' Return winner of the game '''
    p1, p2 = player.score, player_ai.score
    if not player_ai_death and not player_death:
        pass
    elif not player_death:
        p2 += 5
    elif not player_ai_death:
        p1 += 5
    return "player1" if p1 > p2 else "player2" if p2 > p1 else "tie"

if __name__ == "__main__":
    main() 