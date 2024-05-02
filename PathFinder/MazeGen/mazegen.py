import random

def initialize_maze(width, height):
    return [['u' for _ in range(width)] for _ in range(height)]


def surroundingCells(maze, rand_wall, width, height):
    s_cells = 0
    if rand_wall[0] > 0:  
        if maze[rand_wall[0] - 1][rand_wall[1]] == 'c':
            s_cells += 1
    if rand_wall[0] < height-1:  
        if maze[rand_wall[0] + 1][rand_wall[1]] == 'c':
            s_cells += 1
    if rand_wall[1] > 0:  
        if maze[rand_wall[0]][rand_wall[1] - 1] == 'c':
            s_cells += 1
    if rand_wall[1] < width-1:  
        if maze[rand_wall[0]][rand_wall[1] + 1] == 'c':
            s_cells += 1
    return s_cells


def choose_starting_point(maze, width, height):
    starting_height = int(random.random() * height)
    starting_width = int(random.random() * width)
    if starting_height == 0:
        starting_height += 1
    if starting_height == height - 1:
        starting_height -= 1
    if starting_width == 0:
        starting_width += 1
    if starting_width == width - 1:
        starting_width -= 1
    maze[starting_height][starting_width] = 'c'
    return starting_height, starting_width

def initialize_walls(maze, start_height, start_width):
    walls = []
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    for dy, dx in directions:
        ny, nx = start_height + dy, start_width + dx
        maze[ny][nx] = 'w'
        walls.append([ny, nx])
    return walls

def finalize_maze(maze, width, height):
    for i in range(height):
        for j in range(width):
            if maze[i][j] == 'u':
                maze[i][j] = 'w'
    for i in range(width):
        if maze[1][i] == 'c':
            maze[0][i] = 'c'
            break
    for i in range(width - 1, 0, -1):
        if maze[height - 2][i] == 'c':
            maze[height - 1][i] = 'c'
            break
        
def convert_maze(maze):
    conversion = {'w': 1, 'c': 0}
    for i, row in enumerate(maze):
        for j, item in enumerate(row):
            maze[i][j] = conversion.get(item, maze[i][j])

def generate_maze(width, height):
    maze = initialize_maze(width, height)
    start_height, start_width = choose_starting_point(maze, width, height)
    walls = initialize_walls(maze, start_height, start_width)

    while walls:
        rand_wall = walls[int(random.random() * len(walls)) - 1]

        is_valid_wall = True
        if rand_wall[1] != 0:
            if maze[rand_wall[0]][rand_wall[1]-1] == 'u' and maze[rand_wall[0]][rand_wall[1]+1] == 'c':
                s_cells = surroundingCells(maze, rand_wall, width, height)
                if s_cells < 2:
                    maze[rand_wall[0]][rand_wall[1]] = 'c'  
                    if rand_wall[0] != 0:
                        if maze[rand_wall[0]-1][rand_wall[1]] != 'c':
                            maze[rand_wall[0]-1][rand_wall[1]] = 'w'
                            walls.append([rand_wall[0]-1, rand_wall[1]])
                    if rand_wall[0] != height-1:
                        if maze[rand_wall[0]+1][rand_wall[1]] != 'c':
                            maze[rand_wall[0]+1][rand_wall[1]] = 'w'
                            walls.append([rand_wall[0]+1, rand_wall[1]])
                    if rand_wall[1] != width-1:
                        if maze[rand_wall[0]][rand_wall[1]+1] != 'c':
                            maze[rand_wall[0]][rand_wall[1]+1] = 'w'
                            walls.append([rand_wall[0], rand_wall[1]+1])
                else:
                    is_valid_wall = False
            else:
                is_valid_wall = False

        if not is_valid_wall or maze[rand_wall[0]][rand_wall[1]] == 'c':
            walls.remove(rand_wall)

    finalize_maze(maze, width, height)
    convert_maze(maze)
    return maze
