def get_state(player, food, WIDTH, HEIGHT):
    ''' Return game state '''
    state_binary = ( danger_state(player, WIDTH, HEIGHT) + food_state(player.pos, food.pos) + format(player.direction, '02b')) 
    state = int(state_binary, 2)
    return state

def food_state(player_pos, food_pos):
    ''' Return string that represents food position relative to player '''
    player_x, player_y = player_pos
    food_x, food_y = food_pos
    state = ["0", "0", "0", "0"]
    if player_x < food_x:
        state[3] = "1"
    elif player_x > food_x:
        state[2] = "1"
    if player_y < food_y:
        state[0] = "1"
    elif player_y > food_y:
        state[1] = "1"
    state = "".join(state)
    return state

def danger_state(player, WIDTH, HEIGHT):
    ''' Return danger state of all adjacent blocks '''
    x, y = player.pos
    adjacent = [(x, -1 + y), (x, 1 + y), (-1 + x, y), (1 + x, y)]
    adjacent = [check_danger(i, player.grid, player.tail, WIDTH, HEIGHT) for i in adjacent]
    adjacent = "".join(adjacent)
    return adjacent

def check_danger(tup, grid, tail, WIDTH, HEIGHT):
    ''' Verify if specific block is dangerous '''
    x, y = tup
    tup = (x % WIDTH, y % HEIGHT)
    if grid[tup[::-1]] == 1:
        return "1"
    return "0"
  