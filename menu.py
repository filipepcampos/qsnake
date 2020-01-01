import pygame
import singleplayer
import twoplayer
import playerai
import ai
from keypress import register_quit

HEIGHT = 600
WIDTH = 600
images = [pygame.image.load("./assets/menu"+str(i)+".png") for i in range(1, 5)]
modes = ["singleplayer", "ai", "twoplayer", "playerai"]

def main():
    menu()
       
def menu(mainloop=True):    
    pygame.init()    
    pygame.display.set_caption("QSnake")    
    if mainloop:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        screen.blit(images[0], (0, 0))
        pygame.display.flip()
        last_mode, mode = 0, 0
        clock = pygame.time.Clock()
        wait_time, time = 250, 250
        while mainloop:
            time += clock.tick()
            mainloop = not register_quit()
            keys = pygame.key.get_pressed()
            if time > wait_time:
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    mode -= 1
                    time = 0
                elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    mode += 1
                    time = 0
            if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                mainloop = False
                eval(modes[mode % 4] + ".main()")
            
            if mode != last_mode and mainloop:
                screen.blit(images[mode%4], (0, 0))
                pygame.display.flip()
        
    pygame.quit()
        
if __name__ == "__main__":
    main()