import pygame
import numpy as np

WIDTH = 30
HEIGHT = 30
PX_SIZE = 20
REAL_WIDTH = WIDTH * PX_SIZE
REAL_HEIGHT = HEIGHT * PX_SIZE
MAP = "map.csv"

COLORS = {"background": (220, 220, 220),
        "wall": (60, 60, 60)}

def main():
    pygame.init()
    grid = load_map()
    screen = pygame.display.set_mode((REAL_WIDTH, REAL_HEIGHT))
    map_surface = draw_map(grid)    
    
    mainloop = True
    while mainloop:
        screen.blit(map_surface, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False

def load_map():
    if not MAP:
        grid = create_map()
    else:
        grid = np.loadtxt(MAP)
    return grid

def create_map():
    grid = np.zeros((HEIGHT, WIDTH))
    grid[:,0], grid[:,-1] = 1, 1
    grid[0,], grid[-1,] = 1, 1
    # np.savetxt("map.csv", grid, fmt="%.0i")
    return grid

def draw_map(grid):
    surface = pygame.Surface((REAL_WIDTH, REAL_HEIGHT))
    surface.fill(COLORS["background"])
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            if value == 1:
                pygame.draw.rect(surface, COLORS["wall"], pygame.Rect(j*PX_SIZE, i*PX_SIZE, PX_SIZE, PX_SIZE))
    return surface
    


if __name__ == "__main__":
    main() 