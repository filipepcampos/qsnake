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
EPSILON = 0.2
ALPHA = 0.1
GAMMA = 0.9
FPS = 0

# ACTIONS : [UP, DOWN, LEFT, RIGHT]   [0, 1, 2, 3]

def main():  
    q_table = np.zeros((1023, 4))
    mainloop = True
    clock = pygame.time.Clock()  
            
    screen = Screen(WIDTH, HEIGHT, PX_SIZE, MAP)  
    time = 500

    for i in range(1000):
        player = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
        food = Food(WIDTH, HEIGHT, screen.grid) 
        player.change_action(0)
        state = get_state(player, food, WIDTH, HEIGHT)
        time = 500
        mainloop = True
        print(i)

        while mainloop:
            clock.tick(FPS)
            screen.blit(player.pos, food.pos, player.tail) 
            
            reward = 0

            if EPSILON < np.random.uniform():
                action = np.random.choice([0, 1, 2, 3])
            else:
                action = np.argmax(q_table[state])

            player.change_action(action)
            player.move()
            if player.check_food(food):
                reward += 1
                time += 500
            mainloop = player.check_wall() and player.check_tail()
            if not mainloop:
                reward -= 20

            next_state = get_state(player, food, WIDTH, HEIGHT)
            old_value = q_table[state][action]
            next_max = np.max(q_table[next_state])
            new_value = old_value + ALPHA * (reward + GAMMA * next_max - old_value)
            q_table[state][action] = new_value

            state = next_state
            time -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
            print(mainloop)


def register_keypress():
    keys = pygame.key.get_pressed()
    action = None
    if keys[pygame.K_UP]:
        action = 0
    elif keys[pygame.K_DOWN]:
        action = 1
    elif keys[pygame.K_LEFT]:
        action = 2
    elif keys[pygame.K_RIGHT]:
        action = 3
    return action

if __name__ == "__main__":
    main() 