import numpy as np
from collections import deque

class Player:
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

    def check_wall(self):
        ''' Check if player position overlaps a wall\n
        Returns True if so, False otherwise '''
        if self.grid[self.pos] == 1:
            return False
        return True
    
    def check_food(self, food):
        ''' Check if player position overlaps food\n
        Return True, update score and reset food if so, return False otherwise'''
        if self.pos == food.pos:
            food.reset()
            self.score += 1
            return True
        return False
    
    def check_tail(self):
        ''' Check if player position overlaps it's tail\n
        Returns True if so, False otherwise '''
        if self.pos in self.tail:
            return False
        return True
        
    
    def change_action(self, action):
        ''' Change direction based on input action if it's allowed '''
        if action != None:
            if ((self.direction == 0 and action == 1) or (self.direction == 1 and action == 0) or
            (self.direction == 2 and action == 3) or (self.direction == 3 and action == 2)):
                return
            else:
                self.direction = action
        
        
    def move(self):
        ''' Move player along it's direction '''
        #print(f"moving {self.direction}")
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
        while len(self.tail) > self.score:
            self.tail.popleft()

        self.pos = (x%self.map_width, y%self.map_height)
    