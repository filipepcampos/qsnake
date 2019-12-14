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
DATA = "./data/data6/"

GRAPHICS = True
TRAINING = False

# Training parameters
TOTAL = 10_000
EPSILON_DELTA = 1 / TOTAL
ALPHA = 0.1
GAMMA = 0.9
fps = 0

def main():
    fps, mainloop = 60, True
    scores = []
    q_table = load_table()

    if GRAPHICS:
        clock = pygame.time.Clock()
    screen = Screen(WIDTH, HEIGHT, PX_SIZE, MAP, GRAPHICS)  

    epsilon = 1 if TRAINING else 0

    for i in range(TOTAL):
        # Restart game for another round
        player = Player(WIDTH, HEIGHT, PX_SIZE, screen.grid)
        food = Food(WIDTH, HEIGHT, screen.grid)
        player.change_action(0)
        state = get_state(player, food, WIDTH, HEIGHT)
        time = 300
        loop = True

        while mainloop and loop:
            if GRAPHICS:
                clock.tick(fps)

            reward = 0
            
            # Move player and update time
            action = choose_action(epsilon, q_table, state)    
            player.change_action(action)
            player.move()
            time -= 1

            # Attribute reward according to certain conditions
            if player.check_food(food):
                reward += 10
                time += 200
            loop = player.check_death() and time >= 0
            if not loop:
                reward -= 100
            reward -= 0.1

            # Update the screen
            if GRAPHICS and loop:
                screen.blit(player.pos, food.pos, player.tail, player.score) 
            
            # Train the model
            next_state = get_state(player, food, WIDTH, HEIGHT)
            if TRAINING:
                q_table = train(q_table, state, next_state, action, reward, player.score) 
            state = next_state
            
            if GRAPHICS:
                # Register keyboard and quit events
                fps = register_keypress(fps)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        mainloop = False
    
        # Finalize game by appending score and updating epsilon
        epsilon -= EPSILON_DELTA
        scores.append(player.score)
        player.clean_tail()
        if i % 1 == 0:
            print(f"{i}:{player.score}")
        if not mainloop:
            pygame.quit()
            break

    save_data(q_table, scores)

def register_keypress(fps):
    ''' Register keypresses and changes FPS accordingly
    
    Args:
        fps (int): current FPS value
    
    Returns:
        fps (int): new FPS value if key has been pressed
    '''
    keys = pygame.key.get_pressed()
    if keys[pygame.K_4]:
        fps = 0
    elif keys[pygame.K_3]:
        fps = 60
    elif keys[pygame.K_2]:
        fps = 30
    elif keys[pygame.K_1]:
        fps = 10
    return fps

def load_table():
    ''' Load q_table 
    
    Returns:
        q_table (np.array)
    '''
    if not TRAINING:
        q_table = np.load(DATA + "data.npy")
    else:
        q_table = np.zeros((4095, 4))
    return q_table

def choose_action(epsilon, q_table, state):
    ''' Choose which action to take
    
    Args:
        epsilon (float): epsilon value
        q_table (np.array): q_table
        state (int): number that represents current game state

    Returns:
        action (int): number from [0, 1, 2, 3] that represents the next action 
    '''
    if np.random.uniform() < epsilon:
        action = np.random.choice([0, 1, 2, 3])
    else:
        action = np.argmax(q_table[state])
    return action

def train(q_table, state, next_state, action, reward, player_score):
    ''' Perform Q-Learning calculations 
    
    Args:
        q_table (np.array): q_table to be changed
        state (int): number that represents game state before action was taken
        next_state (int): number that represents game state after action was taken
        action (int): last action taken
        reward (int): reward value associated with last action
    
    Returns:
        q_table (np.array): q_table after calculations
    '''
    player_score += 1
    old_value = q_table[state][action]
    next_max = np.max(q_table[next_state])
    new_value = old_value + (player_score/500) * (reward + GAMMA * next_max - old_value)
    q_table[state][action] = new_value
    return q_table

def save_data(q_table, scores):
    ''' Save the data

    Args:
        q_table (np.array): trained numpy array
        scores (np.array): numpy array with score of each round
    '''
    if TRAINING and not GRAPHICS:
        np.save(DATA + "data.npy", q_table)
        np.save(DATA + "scores.npy", np.array(scores))
    if not TRAINING and not GRAPHICS:
        np.save(DATA + "performance.npy", np.array(scores))

if __name__ == "__main__":
    main() 