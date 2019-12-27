import numpy as np
from collections import deque


class Player:
    '''Snake object

    Args:
        WIDTH (int): map width
        HEIGHT (int): map height
        PX_SIZE (int): size of each pixel
        GRID (np.array): grid that represents the map

    Attributes:
        px_size (int): contains value of PX_SIZE
        map_width (int): contains value of WIDTH
        map_height (int): contains value of HEIGHT
        grid (np.array): contains value of GRID
        pos (tuple): player (x, y) coordinates, with x in range(0, map_width) and y in range(0, map_height)
        direction (int): player direction
        tail (deque): contains all positions (tuple) of each block of the tail 
        score (int): quantity of food eaten
    '''
    
    def __init__(self, WIDTH, HEIGHT, PX_SIZE, GRID):
        self.px_size = PX_SIZE
        self.map_width, self.map_height = WIDTH, HEIGHT        
        self.grid = GRID

        self.pos = (np.random.randint(0, WIDTH), np.random.randint(0, HEIGHT))
        while GRID[self.pos] == 1:
            self.pos = (np.random.randint(0, WIDTH), np.random.randint(0, HEIGHT))
        self.direction = None

        self.tail = deque([])
        self.score = 0

    def check_death(self, enemy_pos=None):
        """Check if player position overlaps a wall or tail """
        if self.grid[self.pos[::-1]] == 1 or enemy_pos == self.pos:
            return False
        return True
    
    def check_food(self, food):
        ''' Check if player position overlaps food '''
        if self.pos == food.pos:
            food.reset()
            self.score += 1
            return True
        return False
        
    def change_action(self, action):
        ''' Change direction based on input action if it's allowed '''
        if action != None:
            if ((self.direction == 0 and action == 1) or (self.direction == 1 and action == 0) or
            (self.direction == 2 and action == 3) or (self.direction == 3 and action == 2)):
                return
            else:
                self.direction = action
        
        
    def move(self):
        ''' Update player position according to it's moving direction '''
        x, y = self.pos
        if self.direction == 0:
            y -= 1
        elif self.direction == 1:
            y += 1
        elif self.direction == 2:
            x -= 1
        elif self.direction == 3:
            x += 1

        self.tail.append(self.pos)
        self.grid[self.pos[::-1]] = 1
        while len(self.tail) > self.score:
            tmp = self.tail.popleft()
            self.grid[tmp[::-1]] = 0
        self.pos = (x%self.map_width, y%self.map_height)
    
    def clean_tail(self):
        ''' Remove tail elements from grid '''
        while len(self.tail) > 0:
            tmp = self.tail.popleft()
            self.grid[tmp[::-1]] = 0
    