class DisjointSet:
    def __init__(self, size):
        self.parent = list(range(size))
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            self.parent[rootX] = rootY

def generate_maze_kruskals(width, height):
    cells = height // 2 * width // 2
    ds = DisjointSet(cells)
    maze = [[0 if x % 2 == 1 and y % 2 == 1 else 1 for x in range(width)] for y in range(height)]
    
    edges = []
    for y in range(1, height, 2):
        for x in range(1, width, 2):
            if y > 1:
                edges.append(((x, y), (x, y-2)))
            if x > 1:
                edges.append(((x, y), (x-2, y))) 
    random.shuffle(edges)
    
    for edge in edges:
        cell1, cell2 = edge
        x1, y1 = cell1
        x2, y2 = cell2
        cell1_idx = y1 // 2 * (width // 2) + x1 // 2
        cell2_idx = y2 // 2 * (width // 2) + x2 // 2
        
        if ds.find(cell1_idx) != ds.find(cell2_idx):
            ds.union(cell1_idx, cell2_idx)
            maze[(y1+y2)//2][(x1+x2)//2] = 0

    return maze
