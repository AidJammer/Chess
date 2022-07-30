gameBoard = [['.' for i in range(9)] for j in range(9)]

columns = 'abcdefgh'
rows = '87654321'
pieces = ['r', 'n', 'b', 'k', 'q', 'b', 'n', 'r', 'p']
r_k_moved = {'LR': False, 'RR': False, 'Lr': False, 'Rr': False, 'K': False, 'k': False}
player_Turn = True

for i in range(8):
    curr = i + 1
    gameBoard[1][curr] = pieces[i]
    gameBoard[2][curr] = pieces[8]
    gameBoard[7][curr] = pieces[8].upper()
    gameBoard[8][curr] = pieces[i].upper()
    gameBoard[curr][0] = rows[i]
    gameBoard[0][curr] = columns[i]


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


def valid_move(r, c, new_r, new_c):
    global gameBoard, player_Turn, r_k_moved

    piece_true = gameBoard[r][c]
    sq_val = gameBoard[new_r][new_c]
    piece_low = gameBoard[r][c].lower()
    r_diff = abs(r - new_r)
    c_diff = abs(c - new_c)
    rook = "R" + sq_val if c_diff > c else "L" + sq_val

    if player_Turn and piece_true.islower() or not player_Turn and piece_true.isupper():
        print("Piece selected not valid, please select a valid piece from your side to move.")
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
