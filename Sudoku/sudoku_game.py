import pygame
import sys
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
FONT_SIZE = 40

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGRAY = (200, 200, 200)
HIGHLIGHT_COLOR = (50, 50, 250)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sudoku Game')
font = pygame.font.SysFont(None, FONT_SIZE)

board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + startRow][j + startCol] == num:
                return False
    return True

def solve(board):
    empty = find_empty_location(board)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0
    return False

def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))
    for x in range(0, SCREEN_WIDTH, CELL_SIZE * 3):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT), 3)
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE * 3):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y), 3)

def draw_numbers():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] != 0:
                text = font.render(str(board[row][col]), True, BLACK)
                screen.blit(text, (col * CELL_SIZE + 15, row * CELL_SIZE + 5))

def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  
                    solve(board)

        screen.fill(WHITE)
        draw_grid()
        draw_numbers()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
