r_k_moved = {'LR': False, 'RR': False, 'Lr': False, 'Rr': False, 'K': False, 'k': False}
player_Turn = True
play1_check = False
play2_check = False
play1_mate = False
play2_mate = False
cap_upper = 0
cap_lower = 0


class GameBoard:
    def __init__(self, piece, colour):
        self.piece = piece
        self.colour = colour


class Pieces:
    def __init__(self, move_type, moved):
        self.move_type = move_type
        self.moved = moved

    def legal_move(self, current_square, new_square):
        columns = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        row_diff = abs(int(current_square[1]) - int(new_square[1]))
        col_diff = abs(columns[current_square[0]] - columns[new_square[0]])

        if self.move_type == 'line':
            if self == 'queen' and (row_diff == 0 or col_diff == 0) or (row_diff == col_diff):
                return True
            elif self == 'rook' and (row_diff == 0 or col_diff == 0):
                return True
            elif self == 'bishop' and (row_diff == col_diff):
                return True
            else:
                return False

        if self.move_type == 'single':
            if self == 'pawn' and current_square.colour == "white":



def build_board():
    columns = 'abcdefgh'
    build_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight']

    for i in range(8):
        for j in range(1, 9):
            sq = columns[i] + str(j)
            if sq[1] == '1':
                sq = GameBoard(build_pieces[i], "white")
            elif sq[1] == '2':
                sq = GameBoard("rook", "white")
            elif sq[1] == '7':
                sq = GameBoard("rook", "black")
            elif sq[2] == '8':
                sq = GameBoard(build_pieces[i], "black")
            else:
                sq = GameBoard("none", "none")


# Legal square check
def valid_sq(r, c, new_r, new_c):
    global gameBoard
    cur_sq = gameBoard[r][c]

    try:
        new_sq = gameBoard[new_r][new_c]
        if new_sq == '.' or ((cur_sq.isupper() and new_sq.islower()) or (cur_sq.islower() and new_sq.isupper())):
            return True
        elif (cur_sq == 'k' and new_sq == 'r') or (cur_sq == 'K' and new_sq == 'R'):
            return True
        else:
            return False
    except:
        return False


# Looks for possible piece collisions in movements greater than 1 square
def collision(r, c, new_r, new_c):
    global gameBoard

    player = gameBoard[r][c]

    if player.lower() == 'n':
        return True
    if r == new_r:
        if abs(c-new_c) in {0, 1}:
            return True
        for i in range(c, new_c):
            if gameBoard[r][i + 1] != '.':
                return False
    elif c == new_c:
        if abs(r-new_r) in {0, 1}:
            return True
        for i in range(r, new_r):
            if gameBoard[i + 1][c] != '.':
                return False
    elif (r != new_r) and (c != new_c):
        if abs(r-new_r) in {1, 0} and abs(c-new_c) in {0, 1}:
            return True
        for i, j in zip(range(r, new_r), range(c, new_c)):
            if gameBoard[i][j] != '.':
                return False
    else:
        return True


def sq_under_ass(new_r, new_c):
    global gameBoard

    pieces_checked = 0 + cap_lower if player_Turn else 0 + cap_upper

    while pieces_checked != 16:
        for i in range(1, 8):
            for j in range(1, 8):
                if player_Turn and gameBoard[i][j].islower() and gameBoard[i][j] != '.':
                    if collision(i, j, new_r, new_c) and valid_move(i, j, new_r, new_c):
                        return True
                    else:
                        pieces_checked += 1
                elif not player_Turn and gameBoard[i][j].isupper() and gameBoard[i][j] != '.':
                    if collision(i, j, new_r, new_c) and valid_move(i, j, new_r, new_c):
                        return True
                    else:
                        pieces_checked += 1
    return False


def valid_move(r, c, new_r, new_c):
    global gameBoard, player_Turn, r_k_moved, new_row, new_col, play1_check, play2_check

    piece_true = gameBoard[r][c]
    sq_val = gameBoard[new_r][new_c]
    piece_low = gameBoard[r][c].lower()
    r_diff = abs(r - new_r)
    c_diff = abs(c - new_c)
    rook = "R" + sq_val if c_diff > c else "L" + sq_val

    if player_Turn and piece_true.islower() or not player_Turn and piece_true.isupper():
        print("Piece selected not valid, please select a valid piece from your side to move.")
        return False
    elif (player_Turn and play1_check and piece_true != 'K') or (not player_Turn and play2_check and piece_true != 'k'):
        print("King in check, must move king.")
        return False

    if piece_low == 'p':
        if player_Turn:
            if r < new_r or (r < new_r and c_diff == 1 and sq_val.islower()):
                return True
        elif not player_Turn:
            if r > new_r or (r > new_r and c_diff == 1 and sq_val.isupper()):
                return True

    elif piece_low == 'n':
        if (r_diff == 1 and c_diff == 2) or (r_diff == 2 and c_diff == 1):
            return True

    elif piece_low == 'b':
        if r_diff == c_diff:
            return True

    elif piece_low == 'q':
        if r_diff == c_diff or r_diff == 0 or c_diff == 0:
            return True

    elif piece_low == 'r':
        if r_diff == 0 or c_diff == 0:
            if not r_k_moved[rook]:
                r_k_moved[rook] = True

    elif piece_low == 'k':
        if sq_val.lower() == 'r':
            if player_Turn and sq_val.isupper() and not r_k_moved[piece_true] and not r_k_moved[rook]:
                new_col = c + 2 if c < new_c else c - 2
                for i in range(c, new_col+1):
                    if sq_under_ass(r, i):
                        return False
                r_k_moved[piece_true] = True
                r_k_moved[rook] = True
                return True
            elif not player_Turn and sq_val.islower() and not r_k_moved[piece_true] and not r_k_moved[rook]:
                new_col = c + 2 if c < new_c else c - 2
                for i in range(c, new_col+1):
                    if sq_under_ass(r, i):
                        return False
                r_k_moved[piece_true] = True
                r_k_moved[rook] = True
                return True
        elif r_diff in {1, 0} and c_diff in {0, 1} and not sq_under_ass(new_r, new_c):
            return True


def checkmate(r, c, new_r, new_c):
    global gameBoard, player_Turn, play1_check, play2_check, play1_mate, play2_mate

    play1_done = False
    play2_done = False

    for i in range(1, 8):
        for j in range(1, 8):
            if gameBoard[i][j] == 'k':
                while sq_under_ass(i, j) and not play2_done:
                    if not play2_check:
                        play2_check = True
                    for k in [-1, 0, 1]:
                        for m in [-1, 0, 1]:
                            try:
                                if not sq_under_ass((i+k), (j+m)) and gameBoard[(i+k)][(j+m)] == '.':
                                    play2_done = True
                            except:
                                pass
                    if not play2_done:
                        play2_mate = True

            elif gameBoard[i][j] == 'K':
                while sq_under_ass(i, j) and not play1_done:
                    if not play1_check:
                        play1_check = True
                    for k in [-1, 0, 1]:
                        for m in [-1, 0, 1]:
                            try:
                                if not sq_under_ass((i+k), (j+m)) and gameBoard[(i+k)][(j+m)] == '.':
                                    play1_done = True
                            except:
                                pass
                    if not play1_done:
                        play1_mate = True


# Movement input from player, selected as row and column of piece to move and row, col for square to move to.
# Holds values when legal move is selected.
legal_selects = False
cur_row = 0
cur_col = 0
new_row = 0
new_col = 0

while not legal_selects:
    while cur_row == 0:
        row_input = input("Row of piece to move\n")

        for i, j in enumerate(rows):
            if rows[i] == row_input:
                cur_row = i+1

    while cur_col == 0:
        col_input = input("Column of piece to move\n").lower()

        for i, j in enumerate(columns):
            if columns[i] == col_input:
                cur_col = i+1

    while new_row == 0:
        row_input = input("Row of square to move to\n")

        for i, j in enumerate(rows):
            if rows[i] == row_input:
                new_row = i + 1

    while new_col == 0:
        col_input = input("Column of square to move to\n").lower()

        for i, j in enumerate(columns):
            if columns[i] == col_input:
                new_col = i+1

    if new_row == cur_row and new_col == cur_col:
        print("Invalid move")
        new_row, cur_row, new_col, cur_col = 0, 0, 0, 0
    else:
        if valid_sq(cur_row, cur_col, new_row, new_col) and collision(cur_row, cur_col, new_row, new_col):
            legal_selects = True
        else:
            print("Invalid Move")
            new_row, cur_row, new_col, cur_col = 0, 0, 0, 0



for i in range(9):
    print(*gameBoard[i], sep=' ')
