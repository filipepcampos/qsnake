import pygame

def register_keypress(action=None):
    ''' Register keypresses and changes player action accordingly '''
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        action = 0
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        action = 1
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        action = 2
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        action = 3
    return action

def register_keypress2(direction, direction2):
    ''' Register keypresses and changes player action accordingly
        
    Returns:
        action (int): action corresponding to keypress
    '''
    action, action2 = direction, direction2
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        action = 0
    elif keys[pygame.K_DOWN]:
        action = 1
    elif keys[pygame.K_LEFT]:
        action = 2
    elif keys[pygame.K_RIGHT]:
        action = 3
    if keys[pygame.K_w]:
        action2 = 0
    elif keys[pygame.K_s]:
        action2 = 1
    elif keys[pygame.K_a]:
        action2 = 2
    elif keys[pygame.K_d]:
        action2 = 3
    
    return action, action2

def register_enter():
    ''' Register if ENTER or SPACE has been pressed '''
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
        return True
    return False

def register_quit():    
    ''' Register if QUIT has been pressed '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

def register_esc():
    ''' Register if ESC has been pressed '''
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        return True
    return False