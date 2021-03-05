import pygame, sys, math, random, time, numpy as np

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
AI_LEVEL = 2 #0 = Always random moves, 1 = Picks best available move, 2 = Utilizes minimax algorithm to look ahead
AI_ONLY_GAME = True
STARTING_DEPTH = 1

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
            if (board[r][c] == piece) and (board[r][c + 1] == piece) and (board[r][c + 2] == piece) and (board[r][c + 3] == piece):
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == piece) and (board[r + 1][c] == piece) and (board[r + 2][c] == piece) and (board[r + 3][c] == piece):
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == piece) and (board[r + 1][c + 1] == piece) and (board[r + 2][c + 2] == piece) and (board[r + 3][c + 3] == piece):
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (board[r][c] == piece) and (board[r - 1][c + 1] == piece) and (board[r - 2][c + 2] == piece) and (board[r - 3][c + 3] == piece):
                return True

def score_board(board, piece):
    score = 0
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == piece: score += 12 - 3 * abs(c - 3)
            elif board[r][c] != 0: score -= 8 - 3 * abs(c - 3)
        for c in range(COLUMN_COUNT - 3):
            pcounter = 0
            ocounter = 0
            group = board[r][c:c+4]
            for i in group:
                if i == piece: pcounter += 1
                elif i != 0: ocounter += 1
            if ocounter == 0:
                if pcounter == 4: score += 1000000000  # Giving pieces a score based on horizontal groupings
                elif pcounter == 3: score += 500
                elif pcounter == 2: score += 5
            elif pcounter == 0:
                if ocounter == 4: score -= 1000000000
                elif ocounter == 3: score -= 5000
                elif ocounter == 2: score -= 10
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT):
            pcounter = 0
            ocounter = 0
            group = [board[r][c], board[r+1][c], board[r+2][c], board[r+3][c]]
            for i in group:
                if i == piece: pcounter += 1
                elif i != 0: ocounter += 1
            if ocounter == 0:
                if pcounter == 4: score += 1000000000  # Giving pieces a score based on vertical groupings
                elif pcounter == 3: score += 500
                elif pcounter == 2: score += 5
            elif pcounter == 0:
                if ocounter == 4: score -= 1000000000
                elif ocounter == 3: score -= 5000
                elif ocounter == 2: score -= 10
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            pcounter = 0
            ocounter = 0
            group = [board[r][c], board[r + 1][c + 1], board[r + 2][c + 2], board[r + 3][c + 3]]
            for i in group:
                if i == piece: pcounter += 1
                elif i != 0: ocounter += 1
            if ocounter == 0:
                if pcounter == 4: score += 1000000000  # Giving pieces a score based on positively sloped groupings
                elif pcounter == 3: score += 500
                elif pcounter == 2: score += 5
            elif pcounter == 0:
                if ocounter == 4: score -= 1000000000
                elif ocounter == 3: score -= 5000
                elif ocounter == 2: score -= 10
        for r in range(3, ROW_COUNT):
            pcounter = 0
            ocounter = 0
            group = [board[r][c], board[r - 1][c + 1], board[r - 2][c + 2], board[r - 3][c + 3]]
            for i in group:
                if i == piece: pcounter += 1
                elif i != 0: ocounter += 1
            if ocounter == 0:
                if pcounter == 4: score += 1000000000  # Giving pieces a score based on negatively sloped groupings
                elif pcounter == 3: score += 500
                elif pcounter == 2: score += 5
            elif pcounter == 0:
                if ocounter == 4: score -= 1000000000
                elif ocounter == 3: score -= 5000
                elif ocounter == 2: score -= 10
    return score

def pick_best_move(board, piece, avoid):
    max = -math.inf
    best_column = None
    for c in range(COLUMN_COUNT):
        if c not in avoid and is_valid_location(board, c):
            temp_board = board.copy()
            drop_piece(temp_board, get_next_open_row(temp_board, c), c, piece)
            temp = score_board(temp_board, piece)
            if temp > max:
                max = temp
                best_column = c
    return best_column

def miniMax(board, depth, alpha, beta, piece, maximize):
    col = None
    try: return checked_board_states[checked_board_states.index(board) + 2], checked_board_states[checked_board_states.index(board) + 1]
    except: pass
    if board_is_full(board):
        if maximize: return col, -10000000000000
        else: return col, 10000000000000
    if depth == 0 or winning_move(board, 1) or winning_move(board, 2):
        val = score_board(board, piece)
        checked_board_states.append(board)
        checked_board_states.append(val)
        checked_board_states.append(col)
        return col, val
    if depth == max_depth:
        if board[5][3] == 0 and board[0][0] == 0 and board[0][1] == 0 and board[0][2] == 0 and board[0][4] == 0 and board[0][5] == 0 and board[0][6] == 0: return 3, 0
        for c in range(COLUMN_COUNT):
            if is_valid_location(board, c):
                temp_board = board.copy()
                drop_piece(temp_board, get_next_open_row(temp_board, c), c, piece % 2 + 1)
                if winning_move(temp_board, piece % 2 + 1): return c, 0
                temp_board = board.copy()
                drop_piece(temp_board, get_next_open_row(temp_board, c), c, piece)
                if winning_move(temp_board, piece): return c, 0
    if maximize:
        val = -math.inf
        for c in range(COLUMN_COUNT):
            if is_valid_location(board, c):
                temp_board = board.copy()
                drop_piece(temp_board, get_next_open_row(temp_board, c), c, piece)
                temp_score = miniMax(temp_board, depth-1, alpha, beta, piece, False)[1]
                checked_board_states.append(temp_board)
                checked_board_states.append(temp_score)
                checked_board_states.append(c)
                if temp_score > val:
                    val = temp_score
                    col = c
                if alpha > val: alpha = val
                if alpha >= beta: break
    else:
        val = math.inf
        for c in range(COLUMN_COUNT):
            if is_valid_location(board, c):
                temp_board = board.copy()
                drop_piece(temp_board, get_next_open_row(temp_board, c), c, piece % 2 + 1)
                temp_score = miniMax(temp_board, depth - 1, alpha, beta, piece, True)[1]
                checked_board_states.append(temp_board)
                checked_board_states.append(temp_score)
                checked_board_states.append(c)
                if temp_score < val:
                    val = temp_score
                    col = c
                if beta < val: beta = val
                if alpha >= beta: break
    if depth == max_depth and col == None: print(val)
    return col, val

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1: pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2: pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
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

max_depth = STARTING_DEPTH
result = [None, None, None]
num_play = 0
checked_board_states = []


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0: pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else: pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    if winning_move(board, 1):
                        if PLAYER_ONE == "Player": label = myfont.render("Player 1 wins!!", 1, RED)
                        else: label = myfont.render("Player 2 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                    turn += 1
                    turn = turn % 2
                    num_play += 1
                    print_board(board)
                    draw_board(board)
            elif not AI_GAME:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    if winning_move(board, 2):
                        if PLAYER_ONE == "Player": label = myfont.render("Player 2 wins!!", 1, YELLOW)
                        else: label = myfont.render("Player 1 wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True
                    turn += 1
                    turn = turn % 2
                    num_play += 1
                    print_board(board)
                    draw_board(board)
    if turn == AI and AI_GAME and not game_over:
        if AI_LEVEL == 0: col = random.randint(0, COLUMN_COUNT-1)
        if AI_LEVEL == 1: col = pick_best_move(board, 2)
        if AI_LEVEL == 2:
            t = time.time()
            max_depth = STARTING_DEPTH
            while time.time() - t < 5:
                result = miniMax(board, max_depth, -math.inf, math.inf, 2, True)
                col = result[0]
                print(max_depth)
                max_depth += 1
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            if winning_move(board, 2):
                if PLAYER_ONE == "Player": label = myfont.render("Player 2 wins!!", 1, YELLOW)
                else: label = myfont.render("Player 1 wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True
            turn += 1
            turn = turn % 2
            num_play += 1
            print_board(board)
            draw_board(board)
    if board_is_full(board):
        label = myfont.render('It\'s a tie!', 1, BLUE)
        screen.blit(label, (40, 10))
        game_over = True
    if AI_ONLY_GAME and turn == PLAYER and not game_over:
        if AI_LEVEL == 0: col = random.randint(0, COLUMN_COUNT-1)
        if AI_LEVEL == 1: col = pick_best_move(board, 1)
        if AI_LEVEL == 2:
            t = time.time()
            max_depth = STARTING_DEPTH
            while time.time() - t < 5:
                result = miniMax(board, max_depth, -math.inf, math.inf, 1, True)
                col = result[0]
                print(max_depth)
                max_depth += 1
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)
            if winning_move(board, 1):
                if PLAYER_ONE == "Player": label = myfont.render("Player 2 wins!!", 1, RED)
                else: label = myfont.render("Player 1 wins!!", 1, RED)
                screen.blit(label, (40, 10))
                game_over = True
            turn += 1
            turn = turn % 2
            num_play += 1
            print_board(board)
            draw_board(board)
    if board_is_full(board):
        label = myfont.render('It\'s a tie!', 1, BLUE)
        screen.blit(label, (40, 10))
        game_over = True
    if game_over: pygame.time.wait(3000)