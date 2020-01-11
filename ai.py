import pygame
import numpy as np
from player import Player
from screen import Screen
from food import Food
from get_state import get_state
from keypress import register_quit

WIDTH = 30
HEIGHT = 30
PX_SIZE = 20
#DATA = "./data/3/"
DATA = "./data/1/"
GRAPHICS = True
TRAINING = False

# Training parameters
TOTAL = 30_000
EPSILON_DELTA = 1 / TOTAL
ALPHA = 0.1
GAMMA = 0.90
fps = 0


def main():
    pygame.init()        
    pygame.display.set_caption("QSnake")    
    icon = pygame.image.load("./assets/icon.png")
    pygame.display.set_icon(icon)
    game()
    if GRAPHICS:
        pygame.quit()

def game():
    fps, mainloop = 60, True
    go_to_menu = False
    scores = []
    q_table = load_table()

    if GRAPHICS:
        clock = pygame.time.Clock()
    screen = Screen(WIDTH, HEIGHT, PX_SIZE, None, GRAPHICS)  

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
                screen.blit(player, food) 
            
            # Train the model
            next_state = get_state(player, food, WIDTH, HEIGHT)
            if TRAINING:
                q_table = train(q_table, state, next_state, action, reward, player.score) 
            state = next_state
            
            if GRAPHICS:
                # Register keyboard and quit events
                fps, esc, quit_game = register_events(fps)
                if quit_game:
                    return False
                if esc:
                    return True
                mainloop = not esc
    
        # Finalize game by appending score and updating epsilon
        epsilon -= EPSILON_DELTA
        scores.append(player.score)
        player.clean_tail()
    return False


def register_events(fps=10):
    esc, quit_game = False, False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                esc = True
            elif event.key == pygame.K_1:
                fps = 10
            elif event.key == pygame.K_2:
                fps = 60
            elif event.key == pygame.K_3:
                fps = 110
            elif event.key == pygame.K_4:
                fps = 0
    return fps, esc, quit_game

def load_table():
    ''' Load q_table '''
    if not TRAINING:
        q_table = np.load(DATA + "data.npy")
    else:
        q_table = np.zeros((1023, 4))
    return q_table

def choose_action(epsilon, q_table, state):
    ''' Choose which action to take '''
    if np.random.uniform() < epsilon:
        action = np.random.choice([0, 1, 2, 3])
    else:
        action = np.argmax(q_table[state])
    return action

def train(q_table, state, next_state, action, reward, player_score):
    ''' Perform Q-Learning calculations '''
    old_value = q_table[state][action]
    next_max = np.max(q_table[next_state])
    new_value = old_value + ALPHA * (reward + GAMMA * next_max - old_value)
    q_table[state][action] = new_value
    return q_table

def save_data(q_table, scores):
    ''' Save the data '''
    if TRAINING and not GRAPHICS:
        np.save(DATA + "data.npy", q_table)
        np.save(DATA + "scores.npy", np.array(scores))
    if not TRAINING and not GRAPHICS:
        np.save(DATA + "performance.npy", np.array(scores))

if __name__ == "__main__":
    main() 