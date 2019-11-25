import numpy as np
class Food:
    def __init__(self, WIDTH, HEIGHT, GRID):
        self.width, self.height, self.grid = WIDTH, HEIGHT, GRID
        self.pos = np.random.randint(0, WIDTH), np.random.randint(0, HEIGHT)
        while GRID[self.pos] == 1:
            self.pos = np.random.randint(0, WIDTH), np.random.randint(0, HEIGHT)
    
    def reset(self):
        self.__init__(self.width, self.height, self.grid)