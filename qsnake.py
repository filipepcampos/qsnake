import pygame
import collections
from player import Player
import singleplayer
import twoplayer
import playerai
import ai
from keypress import register_quit

HEIGHT = 600
WIDTH = 600
images = [pygame.image.load("./assets/menu"+str(i)+".png") for i in range(1, 5)]
modes = ["singleplayer", "ai", "twoplayer", "playerai"]
moves = [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
COLORS = {"player": (166, 255, 175),
        "border": (30, 30, 30)}

def main():            
    pygame.init()    
    pygame.display.set_caption("QSnake")

    mainloop, mode = True, 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.blit(images[mode%4], (0, 0))

    pygame.display.flip()
    last_mode = mode
    clock = pygame.time.Clock()
    pos, tail = (3, 27), collections.deque([(3, 23), (3, 24), (3, 25), (3, 26),])
    i = 0
    wait_time, time = 250, 250
    while mainloop:
        time += clock.tick(20)
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
            #mainloop = False
            mainloop = eval(modes[mode % 4] + ".game()")
        
    
        if mainloop:
            i += 1
            pos, tail = update_snake(pos, tail, moves[i%226])
            draw(screen, images[mode%4], pos, tail)
        
    pygame.quit()
        
def draw(screen, img, player_pos,tail):
    ''' Draw snake animation '''

    surface = pygame.Surface((600, 600))
    
    surface.blit(img, (0, 0))
    tmp_rect = pygame.Rect(player_pos[0] * 20, player_pos[1] * 20, 20, 20)
    pygame.draw.rect(surface, COLORS["player"], tmp_rect) 
    pygame.draw.rect(surface, COLORS["border"], tmp_rect, 3)
    for i in tail:
            tmp_rect.x, tmp_rect.y = i[0] * 20, i[1] * 20
            pygame.draw.rect(surface, COLORS["player"], tmp_rect)
            pygame.draw.rect(surface, COLORS["border"], tmp_rect, 3)
    screen.blit(surface, (0, 0))
    pygame.display.flip()

def update_snake(pos, tail, direction):
    ''' Update snake position ''' 
    
    tail.append(pos)
    x, y = pos
    if direction == 0:
        y -= 1
    elif direction == 1:
        y += 1
    elif direction == 2:
        x -= 1
    elif direction == 3:
        x += 1
    tail.popleft()
    return (x, y), tail
    
if __name__ == "__main__":
    main()