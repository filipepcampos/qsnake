import pygame
import numpy as np
from player import Player
from screen import Screen
from food import Food
from get_state import get_state

WIDTH = 30
HEIGHT = 30
PX_SIZE = 20
MAP = "map.csv"
DATA = "./data/data13/"

TOTAL = 1_000
fps = 30

def main():
    mainloop = True
    q_table = np.load(DATA + "data.npy")
    clock = pygame.time.Clock()
    screen = Screen(WIDTH, HEIGHT, PX_SIZE, MAP, True)  


    for i in range(TOTAL):
        # Restart game for another round
        player = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
        player_ai = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
        food = Food(WIDTH, HEIGHT, screen.grid)
        screen.blit(player.pos, food.pos, player.tail, player_ai.pos, player_ai.tail) 
        action = None
        while action == None:            
            action = register_keypress(None)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                    action = 0

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
            loop = player_ai.check_wall() and player_ai.check_tail() and player.check_wall() and player.check_tail()
                   

            # Update the screen
            if loop:
                screen.blit(player.pos, food.pos, player.tail, player_ai.pos, player_ai.tail) 
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
        
        print(f"{player.score}:{player_ai.score}")
        if not mainloop:
            break


def register_keypress(direction):
    ''' Register keypresses and changes player action accordingly
        
    Returns:
        action (int): action corresponding to keypress
    '''
    action = direction
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        action = 0
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        action = 1
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        action = 2
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        action = 3
    return action

if __name__ == "__main__":
    main() 