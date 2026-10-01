import pygame
import math

pygame.init()

ROWS = 6
COLS = 7
SIZE = 100

WIDTH = COLS * SIZE
HEIGHT = (ROWS + 1) * SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

board = [[0 for _ in range(COLS)] for _ in range(ROWS)]


def drop_piece(row, col, piece):
    board[row][col] = piece


def is_valid(col):
    return board[0][col] == 0


def get_row(col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == 0:
            return row


def check_win(piece):
    # horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == piece and \
               board[row][col + 1] == piece and \
               board[row][col + 2] == piece and \
               board[row][col + 3] == piece:
                return True

    # vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == piece and \
               board[row + 1][col] == piece and \
               board[row + 2][col] == piece and \
               board[row + 3][col] == piece:
                return True

    # diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == piece and \
               board[row + 1][col + 1] == piece and \
               board[row + 2][col + 2] == piece and \
               board[row + 3][col + 3] == piece:
                return True

    # diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == piece and \
               board[row - 1][col + 1] == piece and \
               board[row - 2][col + 2] == piece and \
               board[row - 3][col + 3] == piece:
                return True

    return False


def board_full():
    for col in range(COLS):
        if board[0][col] == 0:
            return False
    return True


def minimax(depth, maximizing):
    if check_win(2):
        return 1000

    if check_win(1):
        return -1000

    if depth == 0 or board_full():
        return 0

    if maximizing:
        best = -math.inf

        for col in range(COLS):
            if is_valid(col):
                row = get_row(col)
                board[row][col] = 2

                score = minimax(depth - 1, False)

                board[row][col] = 0

                best = max(best, score)

        return best

    else:
        best = math.inf

        for col in range(COLS):
            if is_valid(col):
                row = get_row(col)
                board[row][col] = 1

                score = minimax(depth - 1, True)

                board[row][col] = 0

                best = min(best, score)

        return best


def ai_move():
    best_score = -math.inf
    best_col = 0

    for col in range(COLS):
        if is_valid(col):
            row = get_row(col)
            board[row][col] = 2

            score = minimax(3, False)

            board[row][col] = 0

            if score > best_score:
                best_score = score
                best_col = col

    return best_col


def draw_board():
    screen.fill(BLACK)

    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(
                screen,
                BLUE,
                (col * SIZE, (row + 1) * SIZE, SIZE, SIZE)
            )

            if board[row][col] == 1:
                color = RED
            elif board[row][col] == 2:
                color = YELLOW
            else:
                color = BLACK

            pygame.draw.circle(
                screen,
                color,
                (col * SIZE + SIZE // 2,
                 (row + 1) * SIZE + SIZE // 2),
                35
            )

    pygame.display.update()


running = True
player_turn = True

while running:
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
            col = event.pos[0] // SIZE

            if col < COLS and is_valid(col):
                row = get_row(col)
                drop_piece(row, col, 1)

                if check_win(1):
                    print("You win!")
                    running = False

                elif board_full():
                    print("Draw!")
                    running = False

                else:
                    player_turn = False

    if not player_turn and running:
        col = ai_move()
        row = get_row(col)
        drop_piece(row, col, 2)

        if check_win(2):
            print("AI wins!")
            running = False

        elif board_full():
            print("Draw!")
            running = False

        else:
            player_turn = True

pygame.quit()