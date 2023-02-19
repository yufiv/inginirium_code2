import pygame

black = [0] * 3
gray = [100] * 3
white = [255] * 3
red = (255, 0, 0)
yellow = (255, 255, 0)
lightgreen = (0, 200, 200)

cross = '#046582'
circle = '#e4bad4'

pygame.init()
width, height = 600, 600
win = pygame.display.set_mode((width, height))

class Board:
    def __init__(self, width, height, size):
        self.width, self.height = width, height
        self.size = size
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        self.move = 1

    def click(self, mouse_pos):
        x = mouse_pos[0] // self.size
        y = mouse_pos[1] // self.size
        self.board[y][x] = self.move
        self.move = -self.move

    def render(self, win):
        pygame.draw.line(win, gray, (0, 200), (self.width, 200))
        pygame.draw.line(win, gray, (0, 400), (self.width, 400))
        pygame.draw.line(win, gray, (200, 0), (200, self.height))
        pygame.draw.line(win, gray, (400, 0), (400, self.height))
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == 1:
                    draw_cross(win, x, y, self.size)
                elif self.board[y][x] == -1:
                    draw_circle(win, x, y, self.size)

    def check_end(self):
        is_end_info = is_end(self.board)
        shift = self.width // 10
        if is_end_info is not None:
            type_end = is_end_info[0]
            number = is_end_info[1]
            if type_end == 'col':
                x0, y0 = (number + .5) * self.size, shift
                x1, y1 = (number + .5) * self.size, self.size * 3 - shift
            elif type_end == 'line':
                x0, y0 = shift, (number + .5) * self.size
                x1, y1 = 3 * self.size - shift, (number + .5) * self.size
            elif type_end == 'diag':
                if number == 1:
                    x0, y0 = shift, shift
                    x1, y1 = 3 * self.size - shift, 3 * self.size - shift
                else:
                    x0, y0 = 3 * self.size - shift, shift
                    x1, y1 = shift, 3 * self.size - shift
            pygame.draw.line(win, red, (x0, y0), (x1, y1), 10)
            pygame.display.update()
            pygame.time.delay(3000)
            return True
        else:
            return False
def draw_circle(win, x, y, size):
    x = (x + .5) * size
    y = (y + .5) * size
    pygame.draw.circle(win, circle, (x, y), (size - 3) // 2, 3)

def draw_cross(win, x, y, size):
    x = x * size + 3
    y = y * size + 3
    pygame.draw.line(win, cross, (x, y), (x + size - 3, y + size - 3), 3)
    pygame.draw.line(win, cross, (x + size - 3, y - 3), (x, y + size - 3), 3)

def is_end(board):
    check_i_line = lambda x, i: True if x[i][0] == x[i][2] != 0 else False
    check_i_col = lambda x, i: True if x[0][i] == x[1][i] == x[2][i] != 0 else False
    check_main_diag = lambda x: True if x[0][0] == x[1][1] == x[2][2] != 0 else False
    check_secondary_diag = lambda x: True if x[0][2] == x[1][1] == x[2][0] != 0 else False
    for i in range(3):
        if check_i_col(board, i):
            return 'col', i
        if check_i_line(board, i):
            return 'line', i
    if check_main_diag(board):
        return 'diag', 1
    if check_secondary_diag(board):
        return 'diag', 2
    return None



board = Board(width, height, 200)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.click(event.pos)
    win.fill(white)
    board.render(win)
    pygame.display.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE] or board.check_end():
        pygame.quit()
        exit()
