import pygame
import numpy as np
class Player:
    def __init__(self, WIDTH, HEIGHT, PX_SIZE):
        self.px_size = PX_SIZE
        # TODO: Verify if player position is not in a wall
        self.pos = (np.random.randint(0, WIDTH), np.random.randint(0, HEIGHT))
        self.direction = None
    
    def load_grid(self, grid):
        self.grid = grid

    def check_wall(self):
        print(self.pos)
        if self.grid[self.pos] == 1:
            return False
        return True
    
    def change_action(self, action):
        if action != None:
            if ((self.direction == 0 and action == 1) or (self.direction == 1 and action == 0) or
            (self.direction == 2 and action == 3) or (self.direction == 3 and action == 2)):
                return
            else:
                self.direction = action
        
    def move(self):
        x, y = self.pos
        if self.direction == 0:
            y -= 1
        elif self.direction == 1:
            y += 1
        elif self.direction == 2:
            x -= 1
        elif self.direction == 3:
            x += 1
        self.pos = (x, y)
    