import numpy as np
class Food:
    ''' Food object '''
    
    def __init__(self, WIDTH, HEIGHT, GRID):
        self.width, self.height, self.grid = WIDTH, HEIGHT, GRID
        self.reset()
    
    def reset(self):
        ''' Reset food position '''
        self.pos = np.random.randint(0, self.width), np.random.randint(0, self.height)
        while self.grid[self.pos[::-1]] == 1:
            self.pos = np.random.randint(0, self.width), np.random.randint(0, self.height)