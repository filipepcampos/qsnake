import pygame
import numpy as np
from player import Player
from screen import Screen
from food import Food
from get_state import get_state
from keypress import register_enter, register_events, register_events2

WIDTH = 30
HEIGHT = 30
PX_SIZE = 20
fps = 15


def main():
    pygame.init()        
    pygame.display.set_caption("QSnake")    
    icon = pygame.image.load("./assets/icon.png")
    pygame.display.set_icon(icon)
    game()
    pygame.quit()

def game():
    mainloop, quit_game = True, False
    clock = pygame.time.Clock()
    screen = Screen(WIDTH, HEIGHT, PX_SIZE, None, True)
    game_map = screen.grid.copy()

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
            action, action2, esc, quit_game = register_events2(player.direction, player2.direction)
            mainloop = not esc
            if quit_game:
                return False

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
            else:
                if not game_map[player.pos[::-1]] and not game_map[player2.pos[::-1]]:
                    col = "" if player_death else "col"
                    col2 = "" if player2_death else "col"
                    screen.blit(player, food, player2, name1="Player1", name2="Player2", collision=col, collision2=col2)
            
            if not loop:
                winner = get_winner(player, player2, player_death, player2_death)
                screen.draw_winner(winner=winner)

        
        player.clean_tail()
        player2.clean_tail()
        mainloop, quit_game = wait_continue(mainloop, quit_game)
        if quit_game:
            return False        
    return True


def wait_start(mainloop):
    ''' Wait for input at the start of the game '''
    action, action2 = None, None
    while (action == None or action2 == None) and mainloop == True:            
        action, action2, esc, quit_game = register_events2(action, action2)
        mainloop = not esc
        if quit_game:
            mainloop = False
    return action, action2, quit_game, mainloop

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

def get_winner(player, player2, player_death, player2_death):
    ''' Return winner of the game '''
    p1, p2 = player.score, player2.score
    if not player2_death and not player_death:
        res = "tie"
    elif not player_death:
        res = "player2" if p1 - p2 <= 10 else "player"
    elif not player2_death:
        res = "player" if p2 - p1 <= 10 else "player2"
    return res


if __name__ == "__main__":
    main() 