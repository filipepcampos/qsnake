import pygame
import numpy as np

COLORS = {"background": (245, 243, 220),
        "wall": (40, 40, 40),        
        "player": (166, 255, 175),
        "player2": (143, 204, 254),
        "winnerplayer1": (95, 244, 112),
        "winnerplayer2": (12, 167, 244),
        "border": (30, 30, 30),
        "food": (255, 141, 103)}

class Screen:
    ''' Handles creation of map grid and drawing of objects

    Args:
        WIDTH (int): map width
        HEIGHT (int): map height
        PX_SIZE (int): size of individual pixel
        MAP (str): relative location to numpy array saved in CSV file. Can be empty
        GRAPHICS (bool): represents if graphics should be active or not

    Attributes:
        width (int): contains the value of WIDTH
        height (int): contains the value of HEIGHT
        real_width (int): contains value of WIDTH in pixels
        real_height (int): contains value of HEIGHT in pixels
        grid (np.array): array that represents the map
        screen (pygame.Surface): window where the game is played
        map_surface (pygame.Surface): surface with all map elements
    '''
    def __init__(self, WIDTH, HEIGHT, PX_SIZE, MAP, GRAPHICS=True):           
        self.width, self.height = WIDTH, HEIGHT
        self.px_size = PX_SIZE
        self.real_width, self.real_height = WIDTH * PX_SIZE, HEIGHT * PX_SIZE        
        self.grid = self.load_map(MAP)
        if GRAPHICS:    
            pygame.init()
            # OpenSansCondensed-Light
            self.font = pygame.font.Font("./assets/OpenSansCondensed-Light.ttf", 32)
            self.screen = pygame.display.set_mode((self.real_width, self.real_height))
            self.map_surface = self.draw_map(self.grid)
        

    def load_map(self, MAP):
        ''' Load map from CSV if it exists, a empty map if not '''
        if MAP:            
            grid = np.loadtxt(MAP)
            if grid.shape != (self.height, self.width):
                grid = self.create_map()            
        else:
            grid = self.create_map()
        return grid

    def create_map(self):
        ''' Create a new map enclosed by walls '''
        grid = np.zeros((self.height, self.width))
        grid[:,0], grid[:,-1] = 1, 1
        grid[0,], grid[-1,] = 1, 1
        return grid

    def draw_map(self, grid):
        ''' Draw all blocks from the map to a surface '''
        surface = pygame.Surface((self.real_width, self.real_height))
        surface.fill(COLORS["background"])
        rows, cols = grid.shape[0], grid.shape[1]
        for x in range(0, rows):
            for y in range(0, cols):
                if grid[x][y] == 1:
                    pygame.draw.rect(surface, COLORS["wall"], pygame.Rect(y*self.px_size, x*self.px_size, self.px_size, self.px_size))
        return surface

    def blit(self, player, food, player2=None, winner=None, name1="Player", name2="Computer"):
        ''' Draw all objects and update the screen '''
        player_pos, tail, player_score = player.pos, player.tail, player.score
        food_pos = food.pos
        if player2:
            player2_pos, tail2, player2_score = player2.pos, player2.tail, player2.score
        surface = self.map_surface.copy()

        # Draw player
        tmp_rect = pygame.Rect(player_pos[0] * self.px_size, player_pos[1] * self.px_size, self.px_size, self.px_size)
        pygame.draw.rect(surface, COLORS["player"], tmp_rect) 
        pygame.draw.rect(surface, COLORS["border"], tmp_rect, 3)

        # Draw food
        tmp_rect.x, tmp_rect.y = food_pos[0] * self.px_size, food_pos[1] * self.px_size
        pygame.draw.rect(surface, COLORS["food"], tmp_rect) 
        pygame.draw.rect(surface, COLORS["border"], tmp_rect, 3)

        # Draw player tail
        for i in tail:
            tmp_rect.x, tmp_rect.y = i[0] * self.px_size, i[1] * self.px_size
            pygame.draw.rect(surface, COLORS["player"], tmp_rect)
            pygame.draw.rect(surface, COLORS["border"], tmp_rect, 3)
        
        # If the game has two players draw the second player
        if player2:
            tmp_rect = pygame.Rect(player2_pos[0] * self.px_size, player2_pos[1] * self.px_size, self.px_size, self.px_size)
            pygame.draw.rect(surface, COLORS["player2"], tmp_rect) 
            pygame.draw.rect(surface, COLORS["border"], tmp_rect, 3)
            for i in tail2:
                tmp_rect.x, tmp_rect.y = i[0] * self.px_size, i[1] * self.px_size
                pygame.draw.rect(surface, COLORS["player2"], tmp_rect)
                pygame.draw.rect(surface, COLORS["border"], tmp_rect, 3)

        text = self.font.render(f"Score: {player_score}", True, COLORS["wall"]) if not player2 else self.font.render(f"{name1}: {player_score}         {name2}: {player2_score}", True, COLORS["wall"])
        text_rect = text.get_rect()
        text_rect.center = (self.real_width // 2, 50)

        self.screen.blit(surface, (0, 0))
        # tmp = pygame.Surface((560, 560))
        # tmp.set_alpha(75)
        # tmp.fill((255, 255, 255))
        # self.screen.blit(tmp, (20, 20))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
    
    def draw_alpha(self, winner=None):
        if winner:
            tmp = pygame.Surface((560, 560))
            tmp.set_alpha(75)
            tmp.fill(COLORS["winner" + winner])
            self.screen.blit(tmp, (20, 20))
            pygame.display.flip()