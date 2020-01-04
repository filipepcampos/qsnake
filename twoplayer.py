import pygame
import numpy as np
from player import Player
from screen import Screen
from food import Food
from get_state import get_state
from keypress import register_enter, register_quit, register_esc
from keypress import register_keypress2 as register_keypress

WIDTH = 30
HEIGHT = 30
PX_SIZE = 20
fps = 20


def main():
    game()
    pygame.quit()

def game():
    mainloop, quit_game = True, False
    clock = pygame.time.Clock()
    screen = Screen(WIDTH, HEIGHT, PX_SIZE, None, True)  

    while mainloop:
        # Restart game for another round
        player = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
        player2 = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
        food = Food(WIDTH, HEIGHT, screen.grid)

        screen.blit(player, food, player2, name1="Player1", name2="Player2") 
        action, action2, quit_game, mainloop = wait_start(mainloop)
        if quit_game:
            return False

        player.change_action(action)
        player2.change_action(action2)
        loop = True

        while mainloop and loop:
            clock.tick(fps)
            old_player_pos, old_player2_pos = player.pos, player2.pos
            # Move player2 and update time
            action, action2 = register_keypress(player.direction, player2.direction)
            player2.change_action(action2)
            player2.move()

            # Move player
            player.change_action(action)
            player.move()

            # Check conditions            
            player.check_food(food)
            player2.check_food(food)
            player2_death, player_death = player2.check_death(player.pos), player.check_death(player2.pos)
            swap = (player.pos == old_player2_pos and player2.pos == old_player_pos)
            if swap:
                player_death, player2_death = False, False
            loop = player2_death and player_death
                               
            # Update the screen
            if loop:
                screen.blit(player, food, player2, name1="Player1", name2="Player2")
            if player2.pos == player.pos:
                screen.blit(player, food, player2, name1="Player1", name2="Player2", collision="col")
            elif swap:
                screen.blit(player, food, player2, name1="Player1", name2="Player2", collision="col", collision2="col")
            
            if not loop:
                winner = get_winner(player, player2, player_death, player2_death)
                screen.draw_winner(winner=winner)
            
            mainloop = not register_esc()
            quit_game = register_quit()
            if quit_game:
                return False
        
        player.clean_tail()
        player2.clean_tail()
        mainloop, quit_game = wait_continue(mainloop, quit_game)
        if quit_game:
            return False        
    return True


def wait_start(mainloop):
    action, action2 = None, None
    while (action == None or action2 == None) and mainloop == True:            
        action, action2 = register_keypress(action, action2)
        quit_game = register_quit()
        mainloop = not register_esc()
        if quit_game:
            mainloop = False
    return action, action2, quit_game, mainloop

def wait_continue(mainloop, quit_game):
    continue_game = False
    while not continue_game and mainloop:
        mainloop = not register_esc()
        continue_game = register_enter()
        quit_game = register_quit()
        if quit_game:
            mainloop = False
    return mainloop, quit_game

def get_winner(player, player2, player_death, player2_death):
    ''' Return winner of the game '''
    p1, p2 = player.score, player2.score
    if not player2_death and not player_death:
        pass
    elif not player_death:
        p2 += 5
    elif not player2_death:
        p1 += 5
    return "player1" if p1 > p2 else "player2" if p2 > p1 else "tie"


if __name__ == "__main__":
    main() 