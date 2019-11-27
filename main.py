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
DATA = ""

GRAPHICS = False
TRAINING = True

TOTAL = 100_000
EPSILON_DELTA = 1 / TOTAL
ALPHA = 0.1
GAMMA = 0.9
fps = 0

# ACTIONS : [UP, DOWN, LEFT, RIGHT]   [0, 1, 2, 3]

def main():
    fps = 60
    scores = []
    if DATA:
        q_table = np.load(DATA)
    else:
        q_table = np.zeros((1023, 4))
    mainloop = True

    if GRAPHICS:
        clock = pygame.time.Clock()
    screen = Screen(WIDTH, HEIGHT, PX_SIZE, MAP, GRAPHICS)  
    time = 200
    if TRAINING:
        epsilon = 1
    else:
        epsilon = 0

    for i in range(TOTAL):
        player = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
        food = Food(WIDTH, HEIGHT, screen.grid)
        player.change_action(0)
        state = get_state(player, food, WIDTH, HEIGHT)
        time = 200
        loop = True

        while mainloop and loop:
            if GRAPHICS:
                clock.tick(fps)
                        
            reward = 0

            if np.random.uniform() < epsilon:
                action = np.random.choice([0, 1, 2, 3])
            else:
                action = np.argmax(q_table[state])
            player.change_action(action)
            player.move()
            time -= 1
            if GRAPHICS:
                screen.blit(player.pos, food.pos, player.tail) 

            if player.check_food(food):
                reward += 1
                time += 100

            loop = player.check_wall() and player.check_tail() and time >= 0
            if not loop:
                reward -= 100
            
            next_state = get_state(player, food, WIDTH, HEIGHT)
            old_value = q_table[state][action]
            next_max = np.max(q_table[next_state])
            new_value = old_value + ALPHA * (reward + GAMMA * next_max - old_value)
            q_table[state][action] = new_value

            state = next_state
            
            if GRAPHICS:
                fps = register_keypress(fps)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        mainloop = False
        epsilon -= EPSILON_DELTA
        scores.append(player.score)
        if i % 500 == 0:
            print(f"{i}:{player.score}")
        if not mainloop:
            break
    if TRAINING and not GRAPHICS:
        np.save("./data/data2/data.npy", q_table)
        np.save("./data/data2/scores.npy", np.array(scores))

def register_keypress(fps):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_4]:
        return 0
    elif keys[pygame.K_3]:
        return 60
    elif keys[pygame.K_2]:
        return 30
    elif keys[pygame.K_1]:
        return 10
    return fps

if __name__ == "__main__":
    main() 