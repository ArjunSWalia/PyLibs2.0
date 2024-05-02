import pygame

def draw_sierpinski(win, vertices, depth):
    if depth == 0:
        pygame.draw.polygon(win, pygame.Color("white"), vertices)
    else:
        mid_points = [((vertices[i][0] + vertices[(i+1) % 3][0]) / 2, (vertices[i][1] + vertices[(i+1) % 3][1]) / 2) for i in range(3)]
        draw_sierpinski(win, [vertices[0], mid_points[0], mid_points[2]], depth-1)
        draw_sierpinski(win, [vertices[1], mid_points[0], mid_points[1]], depth-1)
        draw_sierpinski(win, [vertices[2], mid_points[1], mid_points[2]], depth-1)
