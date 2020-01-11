import pygame
import numpy as np
from player import Player
from screen import Screen
from food import Food
from get_state import get_state
from keypress import register_events, register_enter

WIDTH = 30
HEIGHT = 30
PX_SIZE = 20
DATA = "./data/2/"

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
    q_table = np.load(DATA + "data.npy")
    clock = pygame.time.Clock()
    screen = Screen(WIDTH, HEIGHT, PX_SIZE, None, True)
    game_map = screen.grid.copy()  

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
            action, esc, quit_game = register_events(player.direction)
            mainloop = not esc
            if quit_game:
                return False
            player.change_action(action)
            player.move()

            # Check conditions            
            player.check_food(food)
            player_ai.check_food(food)
            player_ai_death, player_death = player_ai.check_death(player.pos), player.check_death(player_ai.pos)
            swap = (player.pos == old_player_ai_pos and player_ai.pos == old_player_pos)
            if swap:
                player_death, player_ai_death = False, False
            loop = player_ai_death and player_death
                        
            # Update the screen
            if loop: 
                screen.blit(player, food, player_ai)
            else:
                if not game_map[player.pos[::-1]] and not game_map[player_ai.pos[::-1]]:
                    col = "" if player_death else "col"
                    col2 = "" if player_ai_death else "col"
                    screen.blit(player, food, player_ai, collision=col, collision2=col2)

            if not loop:
                winner = get_winner(player, player_ai, player_death, player_ai_death)
                screen.draw_winner(winner=winner)
        
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
        action, esc, quit_game = register_events()  
        mainloop = not esc
        if quit_game:
            mainloop = False
    return action, quit_game, mainloop

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

def get_winner(player, player_ai, player_death, player_ai_death):
    ''' Return winner of the game '''
    p1, p2 = player.score, player_ai.score
    if not player_ai_death and not player_death:
        res = "tie"
    elif not player_death:
        res = "playerai" if p1 - p2 <= 10 else "player"
    elif not player_ai_death:
        res = "player" if p2 - p1 <= 10 else "playerai"
    return res

if __name__ == "__main__":
    main() 