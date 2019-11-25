import pygame
import numpy as np
from player import Player
from screen import Screen

WIDTH = 30
HEIGHT = 30
PX_SIZE = 20
REAL_WIDTH = WIDTH * PX_SIZE
REAL_HEIGHT = HEIGHT * PX_SIZE
MAP = "map.csv"
FPS = 20

# ACTIONS : [UP, DOWN, LEFT, RIGHT]   [0, 1, 2, 3]

def main():
    pygame.init()
    screen = Screen(WIDTH, HEIGHT, PX_SIZE, MAP)
    player = Player(WIDTH, HEIGHT, PX_SIZE)
    player.load_grid(screen.grid)    
    mainloop = True
    clock = pygame.time.Clock()

    while mainloop:
        clock.tick(FPS)
        screen.blit(player.pos) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False

        action = register_keypress()
        player.change_action(action)
        player.move()

        mainloop = player.check_wall()


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