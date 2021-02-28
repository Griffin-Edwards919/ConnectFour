import numpy as np
import pygame
import sys
import math
import random

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1
AI_GAME = True
PLAYER_ONE = None
AI_LEVEL = 1 #0 = Always random moves, 1 = Picks best available move, 2 = Utilizes minimax algorithm to look ahead

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def score_board(board, piece):
    score = 0
    pcounter = 0
    ocounter = 0
    for row in board:
        for c in range(COLUMN_COUNT):
            if row[c] == piece: score += 3 - abs(c - 3) #Giving pieces a score for being closer to the middle
            elif row[c] == piece % 2 + 1: score -= 3 - abs(c - 3)
        for c in range(COLUMN_COUNT - 3):
            group = row[c:c+4]
            for i in group:
                if(i == piece): pcounter+=1
                elif(i == piece % 2 + 1): ocounter+=1
            if ocounter == 0:
                if pcounter == 4: score += 10000 #Giving pieces a score based on horizontal groupings
                elif pcounter == 3: score += 10
                elif pcounter == 2: score += 5
            if pcounter == 0:
                if ocounter == 4: score -= 10000
                elif ocounter == 3: score -= 50
                elif ocounter == 2: score -= 10
            ocounter = 0;
            pcounter = 0;
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT):
            group = [board[r][c], board[r+1][c], board[r+2][c], board[r+3][c]]
            for i in group:
                if (i == piece): pcounter += 1
                elif (i == piece % 2 + 1): ocounter += 1
            if ocounter == 0:
                if pcounter == 4: score += 10000  # Giving pieces a score based on vertical groupings
                elif pcounter == 3: score += 10
                elif pcounter == 2: score += 5
            if pcounter == 0:
                if ocounter == 4: score -= 10000
                elif ocounter == 3: score -= 50
                elif ocounter == 2: score -= 10
            ocounter = 0;
            pcounter = 0;
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            group = [board[r][c], board[r + 1][c + 1], board[r + 2][c + 2], board[r + 3][c + 3]]
            for i in group:
                if (i == piece): pcounter += 1
                elif (i == piece % 2 + 1): ocounter += 1
            if ocounter == 0:
                if pcounter == 4: score += 10000  # Giving pieces a score based on positively sloped groupings
                elif pcounter == 3: score += 10
                elif pcounter == 2: score += 5
            if pcounter == 0:
                if ocounter == 4: score -= 10000
                elif ocounter == 3: score -= 50
                elif ocounter == 2: score -= 10
            ocounter = 0;
            pcounter = 0;
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            group = [board[r][c], board[r - 1][c + 1], board[r - 2][c + 2], board[r - 3][c + 3]]
            for i in group:
                if (i == piece): pcounter += 1
                elif (i == piece % 2 + 1): ocounter += 1
            if ocounter == 0:
                if pcounter == 4: score += 10000  # Giving pieces a score based on negatively sloped groupings
                elif pcounter == 3: score += 10
                elif pcounter == 2: score += 5
            if pcounter == 0:
                if ocounter == 4: score -= 10000
                elif ocounter == 3: score -= 50
                elif ocounter == 2: score -= 10
            ocounter = 0;
            pcounter = 0;
    return score

def pick_best_move(board, piece):
    max = -10000000
    best_column = -1
    for c in range(COLUMN_COUNT):
        if(is_valid_location(board, c)):
            temp_board = board.copy()
            drop_piece(temp_board, get_next_open_row(temp_board, c), c, piece)
            temp = score_board(temp_board, piece)
            print(c, temp)
            if temp > max:
                max = temp
                best_column = c
    return best_column


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def board_is_full(board):
    for row in board:
        for column in row:
            if column == 0: return False
    return True

board = create_board()
print_board(board)
game_over = False
turn = random.randint(0,1)
if turn == 0: PLAYER_ONE = "Player"

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        if PLAYER_ONE == "Player":
                            label = myfont.render("Player 1 wins!!", 1, RED)
                        else:
                            label = myfont.render("Player 2 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)

            elif not AI_GAME:
                # # Ask for Player 2 Input
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        if PLAYER_ONE == "Player":
                            label = myfont.render("Player 2 wins!!", 1, RED)
                        else:
                            label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)

    if turn == AI and AI_GAME and not game_over:

        if AI_LEVEL == 0: col = random.randint(0, COLUMN_COUNT-1)
        if AI_LEVEL == 1: col = pick_best_move(board, 2)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                if PLAYER_ONE == "Player":
                    label = myfont.render("Player 2 wins!!", 1, YELLOW)
                else:
                    label = myfont.render("Player 1 wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            turn += 1
            turn = turn % 2

            print_board(board)
            draw_board(board)

    if board_is_full(board):
        label = myfont.render('It\'s a tie!', 1, BLUE)
        screen.blit(label, (40, 10))
        game_over = True

    if game_over:
        pygame.time.wait(3000)