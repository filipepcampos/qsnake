import pygame
import numpy as np

COLORS = {"background": (220, 220, 220),
        "wall": (60, 60, 60),
        "player": (0, 200, 0)}

class Screen:
    def __init__(self, WIDTH, HEIGHT, PX_SIZE, MAP):
        self.width, self.height = WIDTH, HEIGHT
        self.px_size = PX_SIZE
        self.real_width, self.real_height = WIDTH * PX_SIZE, HEIGHT * PX_SIZE


        self.screen = pygame.display.set_mode((self.real_width, self.real_height))
        self.grid = self.load_map(MAP)
        self.surface = self.draw_map(self.grid)

        self.player_rect = pygame.Rect(0, 0, PX_SIZE, PX_SIZE)

    def load_map(self, MAP):
        if not MAP:
            grid = self.create_map()
        else:
            # Todo: check if dimensions = map dimensions
            grid = np.loadtxt(MAP)
        return grid

    def create_map(self):
        grid = np.zeros((HEIGHT, WIDTH))
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

    def blit(self, player_pos):
        self.surface = self.draw_map(self.grid)
        self.player_rect.x, self.player_rect.y = player_pos
        self.player_rect.x *= self.px_size
        self.player_rect.y *= self.px_size
        pygame.draw.rect(self.surface, COLORS["player"], self.player_rect)   
        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()