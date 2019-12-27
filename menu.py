import pygame
import singleplayer
import twoplayer
import playerai
import ai

HEIGHT = 600
WIDTH = 600

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill((245, 243, 220))
    screen.blit(surface, (0, 0))
    mainloop = True
    while mainloop:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            mainloop = False
            singleplayer.main()
        elif keys[pygame.K_2]:
            mainloop = False
            ai.main()
        elif keys[pygame.K_3]:
            mainloop = False
            twoplayer.main()
        elif keys[pygame.K_4]:
            mainloop = False
            playerai.main()
    pygame.quit()
        



if __name__ == "__main__":
    main()