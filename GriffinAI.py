import time, math, numpy

STARTING_DEPTH = 1
checked_board_states = []
max_depth = STARTING_DEPTH
ROW_COUNT = 6
COLUMN_COUNT = 7

def get_move(board, piece):
    global max_depth, checked_board_states
    t = time.time()
    max_depth = STARTING_DEPTH
    while time.time() - t < 1.9:
        col = miniMax(board, max_depth, -math.inf, math.inf, piece, True)[0]
        max_depth += 1
    return col

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
    return col, val

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

def board_is_full(board):
    for row in board:
        for column in row:
            if column == 0: return False
    return True


def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

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