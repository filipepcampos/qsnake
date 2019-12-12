def get_state(player, food, WIDTH, HEIGHT):
    ''' Return game state
    
    Args:
        player (Player): player object
        food (Food): food object
        WIDTH (int): map width
        HEIGHT (int): map height
    
    Returns:
        state (int): Unique number that represents current state 
    '''
    state_binary = danger_state(player, WIDTH, HEIGHT) + food_state(player.pos, food.pos) + format(player.direction, '02b')
    state = int(state_binary, 2)
    return state

def food_state(player_pos, food_pos):
    ''' Return string that represents food position relative to player
    
    Args:
        player_pos (tuple): player position
        food_pos (tuple): food position
        
    Returns:
        state (str): string that represents 4 boolean values (food_left, food_right, food_up, food_down)
    '''
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
    ''' Return danger state of all adjacent blocks
    
    Args:
        player (Player): player object
        WIDTH (int): map width
        HEIGHT (int): map height
        
    Returns:
        adjacent (str): string that represents 4 boolean values corresponding to the danger in 4 possible movement directions
    '''
    x, y = player.pos
    adjacent = [(x, -1 + y), (x, 1 + y), (-1 + x, y), (1 + x, y)]
    adjacent = [check_danger(i, player.grid, player.tail, WIDTH, HEIGHT) for i in adjacent]
    adjacent = "".join(adjacent)
    return adjacent

def check_danger(tup, grid, tail, WIDTH, HEIGHT):
    ''' Verify if specific block is dangerous
    
    Args:
        tup (tuple): block position in (x, y) coordinates
        grid (np.array): numpy array that represents the map
        tail (collections.deque): contains all (x, y) positions of the tail blocks
        WIDTH (int): map width
        HEIGHT (int): map height
    
    Returns:
        (str): "1" if block is dangerous, "0" if not
    '''
    x, y = tup
    tup = (x % WIDTH, y % HEIGHT)
    if grid[tup[::-1]] == 1:
        return "1"
    return "0"
  