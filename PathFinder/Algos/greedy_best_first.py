def greedy_best_first(draw, grid, start, end):
    count = 0
    open_set = CustomPriorityQueue()
    open_set.put(start, 0)
    came_from = {}
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in open_set_hash:
                count += 1
                priority = h(neighbor.get_pos(), end.get_pos())
                open_set.put(neighbor, priority)
                came_from[neighbor] = current
                open_set_hash.add(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False
