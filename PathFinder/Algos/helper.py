import pygame

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cell = grid[row][col]
                if not start and cell != end:
                    start = cell
                    start.make_start()

                elif not end and cell != start:
                    end = cell
                    end.make_end()

                elif cell != end and cell != start:
                    cell.make_barrier()

            elif pygame.mouse.get_pressed()[2]: 
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cell = grid[row][col]
                cell.reset()
                if cell == start:
                    start = None
                elif cell == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end and not started:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()    
    
    def get_algorithm(key, start, end, draw, grid):
        if key == pygame.K_a:  
        return lambda: a_star_algorithm(draw, grid, start, end), "A* Algorithm"
    elif key == pygame.K_d:  
        return lambda: dijkstra(draw, grid, start, end), "Dijkstra's Algorithm"
    elif key == pygame.K_g:  
        return lambda: greedy_best_first(draw, grid, start, end), "Greedy Best-First Search"
    return None, ""

