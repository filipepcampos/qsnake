def get_state(player, food, WIDTH, HEIGHT):
    return int(danger_state(player, WIDTH, HEIGHT) + food_state(player.pos, food.pos) + str(bin(player.direction))[2:], 2)

def food_state(player_pos, food_pos):
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

def danger_state(player, WIDTH, HEIGHT):
    x, y = player.pos
    grid = player.grid
    tail = player.tail
    adjacent = [(-1 + x, 0), (1 + x, 0), (0, -1 + y), (0, 1 + y)]
    adjacent = map(lambda x: check_danger(x, grid, tail, WIDTH, HEIGHT), adjacent)
    return "".join(adjacent)

def check_danger(tup, grid, tail, WIDTH, HEIGHT):
    x, y = tup
    tup = (x % WIDTH, y % HEIGHT)
    if grid[tup] == 1:
        return "1"
    elif tup in tail:
        return "1"
    return "0"
  