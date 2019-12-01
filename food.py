import numpy as np
class Food:
    ''' Food object

    Args:
        WIDTH (int): map width
        HEIGHT (int): map height
        grid (np.array): numpy array that represents the map
    
    Attributes:
        width (int): contains the value of WIDTH
        height (int): contains the value of HEIGHT
        grid (np.array): contains the value of GRID
        pos (tuple): food (x, y) position
    '''
    def __init__(self, WIDTH, HEIGHT, GRID):
        self.width, self.height, self.grid = WIDTH, HEIGHT, GRID
        self.reset()
    
    def reset(self, tail=[]):
        ''' Reset food position
        
        Args:
            tail (collections.deque): optional deque containing player's tail (x, y) positions
        '''
        self.pos = np.random.randint(0, self.width), np.random.randint(0, self.height)
        while self.grid[self.pos[::-1]] == 1 or self.pos in tail:
            self.pos = np.random.randint(0, self.width), np.random.randint(0, self.height)