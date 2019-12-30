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
fps = 20

def main():
    mainloop = True
    clock = pygame.time.Clock()
    screen = Screen(WIDTH, HEIGHT, PX_SIZE, None, True)  

    while True:
        # Restart game for another round
        player = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
        player2 = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
        food = Food(WIDTH, HEIGHT, screen.grid)
        screen.blit(player, food, player2, name1="Player1", name2="Player2") 
        action, action2 = None, None
        while (action == None or action2 == None) and mainloop == True:            
            action, action2, go_to_menu = register_keypress(action, action2)
            mainloop = register_quit()
            if go_to_menu:
                mainloop = False

        player.change_action(action)
        player2.change_action(action2)
        loop = True

        while mainloop and loop:
            clock.tick(fps)
            # Move player2 and update time
            action, action2, go_to_menu = register_keypress(player.direction, player2.direction)
            player2.change_action(action2)
            player2.move()

            # Move player
            player.change_action(action)
            player.move()

            # Check conditions            
            player.check_food(food)
            player2.check_food(food)
            player2_death, player_death = player2.check_death(player.pos), player.check_death(player2.pos)
            loop = player2_death and player_death
            if not player2_death and not player_death:
                print("Tie")
            elif not player_death:
                print("AI wins")
            elif not player2_death:
                print("Player wins")
                   
            # Update the screen
            if loop or (not player2_death and not player_death):
                screen.blit(player, food, player2, name1="Player1", name2="Player2")
            
            mainloop = register_quit()
            if go_to_menu:
                loop, mainloop = False, False
        
        player.clean_tail()
        player2.clean_tail()
        continue_game = False
        if go_to_menu:
            menu.main()
        while not continue_game and mainloop:
            mainloop = register_quit()
            continue_game = register_enter()
            _, _, go_to_menu = register_keypress(None, None)
            if go_to_menu:
                mainloop = False
                menu.main()
        
        if not mainloop:
            pygame.quit()
            break


def register_keypress(direction, direction2):
    ''' Register keypresses and changes player action accordingly
        
    Returns:
        action (int): action corresponding to keypress
    '''
    action, action2 = direction, direction2
    go_to_menu = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        action = 0
    elif keys[pygame.K_DOWN]:
        action = 1
    elif keys[pygame.K_LEFT]:
        action = 2
    elif keys[pygame.K_RIGHT]:
        action = 3
    if keys[pygame.K_w]:
        action2 = 0
    elif keys[pygame.K_s]:
        action2 = 1
    elif keys[pygame.K_a]:
        action2 = 2
    elif keys[pygame.K_d]:
        action2 = 3
    if keys[pygame.K_ESCAPE]:
        go_to_menu = True
    
    return action, action2, go_to_menu

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