import pygame
import numpy as np

COLORS = {"background": (220, 220, 220),
        "wall": (60, 60, 60),
        "player": (0, 200, 0),
        "border": (30, 30, 30),
        "food": (200, 0, 0)}

class Screen:
    def __init__(self, WIDTH, HEIGHT, PX_SIZE, MAP):        
        pygame.init()
        self.width, self.height = WIDTH, HEIGHT
        self.px_size = PX_SIZE
        self.real_width, self.real_height = WIDTH * PX_SIZE, HEIGHT * PX_SIZE


        self.screen = pygame.display.set_mode((self.real_width, self.real_height))
        self.grid = self.load_map(MAP)
        self.surface = self.draw_map(self.grid)

    def load_map(self, MAP):
        if MAP:            
            grid = np.loadtxt(MAP)
            if grid.shape != (self.height, self.width):
                grid = self.create_map()            
        else:
            grid = self.create_map()
        return grid

    def create_map(self):
        grid = np.zeros((self.height, self.width))
        grid[:,0], grid[:,-1] = 1, 1
        grid[0,], grid[-1,] = 1, 1
        # np.savetxt("map.csv", grid, fmt="%.0i")
        return grid

    def draw_map(self, grid):
        surface = pygame.Surface((self.real_width, self.real_height))
        surface.fill(COLORS["background"])
        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                if value == 1:
                    pygame.draw.rect(surface, COLORS["wall"], pygame.Rect(j*self.px_size, i*self.px_size, self.px_size, self.px_size))
        return surface

    def blit(self, player_pos, food_pos, tail):
        self.surface = self.draw_map(self.grid)

        tmp_rect = pygame.Rect(player_pos[0] * self.px_size, player_pos[1] * self.px_size, self.px_size, self.px_size)
        pygame.draw.rect(self.surface, COLORS["player"], tmp_rect) 
        pygame.draw.rect(self.surface, COLORS["border"], tmp_rect, 3)

        tmp_rect.x, tmp_rect.y = food_pos[0] * self.px_size, food_pos[1] * self.px_size
        pygame.draw.rect(self.surface, COLORS["food"], tmp_rect) 
        pygame.draw.rect(self.surface, COLORS["border"], tmp_rect, 3)

        for i in tail:
            tmp_rect.x, tmp_rect.y = i[0] * self.px_size, i[1] * self.px_size
            pygame.draw.rect(self.surface, COLORS["player"], tmp_rect)
            pygame.draw.rect(self.surface, COLORS["border"], tmp_rect, 3)
        
        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()