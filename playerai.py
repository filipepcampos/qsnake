import pygame
import numpy as np
from player import Player
from screen import Screen
from food import Food
from get_state import get_state
import menu

WIDTH = 30
HEIGHT = 30
PX_SIZE = 20
MAP = "map.csv"
DATA = "./data/data13/"

fps = 20

def main():
    mainloop, go_to_menu = True, False
    q_table = np.load(DATA + "data.npy")
    clock = pygame.time.Clock()
    screen = Screen(WIDTH, HEIGHT, PX_SIZE, MAP, True)  


    while True:
        # Restart game for another round
        player = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
        player_ai = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
        food = Food(WIDTH, HEIGHT, screen.grid)
        screen.blit(player.pos, food.pos, player.tail, player.score, player_ai.pos, player_ai.tail, player_ai.score) 
        action = None
        while action == None and mainloop == True:            
            action, go_to_menu = register_keypress(None)
            mainloop = register_quit()
            if go_to_menu:
                mainloop = False

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
            action, go_to_menu = register_keypress(player.direction)
            player.change_action(action)
            player.move()

            # Check conditions            
            player.check_food(food)
            player_ai.check_food(food)
            player_ai_death, player_death = player_ai.check_death(player.pos), player.check_death(player_ai.pos)
            loop = player_ai_death and player_death
            if not player_ai_death and not player_death:
                print("Tie")
            elif not player_death:
                print("AI wins")
            elif not player_ai_death:
                print("Player wins")

                     
            # Update the screen
            if loop or (not player_ai_death and not player_death):
                screen.blit(player.pos, food.pos, player.tail, player.score, player_ai.pos, player_ai.tail, player_ai.score)
            
            mainloop = register_quit()
            if go_to_menu:
                loop, mainloop = False, False
        
        print(f"{player.score}:{player_ai.score}")
        player.clean_tail()
        player_ai.clean_tail()
        continue_game = False
        if go_to_menu:
            menu.main()
        while not continue_game and mainloop:
            mainloop = register_quit()
            continue_game = register_enter()
            _, go_to_menu = register_keypress(None)
            if go_to_menu:
                mainloop = False
                menu.main()
        
        if not mainloop:
            pygame.quit()
            break


def register_keypress(direction):
    ''' Register keypresses and changes player action accordingly
        
    Returns:
        action (int): action corresponding to keypress
    '''
    action, go_to_menu = direction, False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        action = 0
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        action = 1
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        action = 2
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        action = 3
    elif keys[pygame.K_ESCAPE]:
        go_to_menu = True
    return action, go_to_menu

def register_enter():
    ''' Register if ENTER has been pressed
    
    Returns:
        (bool): True if key has been pressed'''
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
        return True
    return False

def register_quit():    
    ''' Register if QUIT has been pressed
    
    Returns:
        (bool): True if button hasn't been pressed'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

if __name__ == "__main__":
    main() 