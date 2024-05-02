def dijkstra(draw, grid, start, end):
    count = 0
    open_set = CustomPriorityQueue()
    open_set.put(start, 0)
    came_from = {}
    distance = {cell: float("inf") for row in grid for cell in row}
    distance[start] = 0

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
            temp_distance = distance[current] + 1

            if temp_distance < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = temp_distance
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put(neighbor, distance[neighbor])
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False
