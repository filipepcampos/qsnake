def get_state(player, food, WIDTH, HEIGHT):
    ''' Return game state '''
    state_binary = danger_state(player, WIDTH, HEIGHT) + center_state(player) +food_state(player.pos, food.pos) + format(player.direction, '02b')
    return int(state_binary, 2)

def food_state(player_pos, food_pos):
    ''' Return string corresponding to food state (relative to player) '''
    player_x, player_y = player_pos
    food_x, food_y = food_pos
    # is_up, is_down , is_left, is_right
    state = ["0", "0", "0", "0"]
    if player_x < food_x:
        state[3] = "1"
    elif player_x > food_x:
        state[2] = "1"
    if player_y < food_y:
        state[0] = "1"
    elif player_y > food_y:
        state[1] = "1"
    return "".join(state)

def center_state(player):
    tail = player.tail
    pos = player.pos
    center_x, center_y = sum([x for x, y in tail]), sum([y for x, y in tail])    
    is_up, is_left = "0", "0"
    if center_x > pos[0]:
        is_left = "1"
    if center_y < pos[1]:
        is_up = "1"
    return is_up + is_left

def danger_state(player, WIDTH, HEIGHT):
    ''' Return string corresponding to the adjacent blocks which are dangerous '''
    x, y = player.pos
    grid = player.grid
    tail = player.tail
    adjacent = [(x, -1 + y), (x, 1 + y), (-1 + x, y), (1 + x, y)]
    adjacent = [check_danger(i, grid, tail, WIDTH, HEIGHT) for i in adjacent]
    return "".join(adjacent)

def check_danger(tup, grid, tail, WIDTH, HEIGHT):
    ''' Verify if coordinates contain danger '''
    x, y = tup
    tup = (x % WIDTH, y % HEIGHT)
    if grid[tup] == 1 or tup in tail:
        return "1"
    return "0"
  