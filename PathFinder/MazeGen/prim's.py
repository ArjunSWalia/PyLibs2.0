import random
def recursive_division(maze, x, y, width, height, orientation):
    if width < 2 or height < 2:
        return

    horizontal = orientation == 'H'
    wx = x + (0 if horizontal else random.randint(0, width - 2))
    wy = y + (random.randint(0, height - 2) if horizontal else 0)
    px = wx + (0 if horizontal else random.randint(0, width - 2))
    py = wy + (random.randint(0, height - 2) if horizontal else 0)

    dx = 1 if horizontal else 0
    dy = 0 if horizontal else 1
    length = width if horizontal else height
    next_orientation = 'V' if orientation == 'H' else 'H'

    for i in range(length):
        if wx != px or wy != py:
            maze[wy][wx] = 1
        wx += dx
        wy += dy

    divide_x, divide_y = x, y
    divide_width, divide_height = (width, wy-y) if horizontal else (wx-x, height)
    recursive_division(maze, divide_x, divide_y, divide_width, divide_height, next_orientation)

    divide_x, divide_y = (x, wy+1) if horizontal else (wx+1, y)
    divide_width, divide_height = (width, y+height-wy-1) if horizontal else (x+width-wx-1, height)
    recursive_division(maze, divide_x, divide_y, divide_width, divide_height, next_orientation)

def generate_maze_recursive_division(width, height):
    maze = [[0 for _ in range(width)] for _ in range(height)]
    for i in range(width):
        maze[0][i] = maze[height-1][i] = 1
    for i in range(height):
        maze[i][0] = maze[i][width-1] = 1

    recursive_division(maze, 1, 1, width-2, height-2, 'H' if random.choice([True, False]) else 'V')
    return maze
