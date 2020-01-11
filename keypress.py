import pygame

def register_events(action = None):
    esc, quit_game = False, False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                esc = True
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                action = 0
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                action = 1
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                action = 2
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                action = 3
    return action, esc, quit_game

def register_events2(direction, direction2):
    ''' Register keypresses and changes player action accordingly '''
    esc, quit_game = False, False
    action, action2 = direction, direction2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                esc = True
            elif event.key == pygame.K_UP:
                action = 0
            elif event.key == pygame.K_DOWN:
                action = 1
            elif event.key == pygame.K_LEFT:
                action = 2
            elif event.key == pygame.K_RIGHT:
                action = 3
            elif event.key == pygame.K_w:
                action2 = 0
            elif event.key == pygame.K_s:
                action2 = 1
            elif event.key == pygame.K_a:
                action2 = 2
            elif event.key == pygame.K_d:
                action2 = 3
    return action, action2, esc, quit_game
    
def register_enter():
    ''' Register if ENTER or SPACE has been pressed '''
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
        return True
    return False

def register_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False