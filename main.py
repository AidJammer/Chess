player_Turn = True
play1_check = False
play2_check = False
play1_mate = False
play2_mate = False
cap_white = 0
cap_black = 0

threats = {}


class GameBoard:
    def __init__(self, piece, colour, moved):
        self.piece = piece
        self.colour = colour
        self.moved = moved

        print(self.piece)

    def valid_square(self, current_square):
        if self.piece == "none" or (current_square.colour == "white" and self.colour == "black")\
                                or (current_square.colour == "black" and self.colour == "white"):
            return True
        else:
            return False


class Pieces:
    def __init__(self, move_type):
        self.move_type = move_type

    def valid_capture(self, current_square, new_square):
        if new_square.colour != current_square.colour:
            return True
        return False

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

        elif self.move_type == 'single':
            if self == 'pawn' and current_square.colour == "white":
                if (int(current_square[1]) + 1) == int(new_square[1]):
                    return True
                elif (int(current_square[1]) + 1) == int(new_square[1]) \
                        and (columns[current_square[0]] + 1) == columns[new_square[0]] \
                        and self.valid_capture(current_square, new_square):
                    return True
            elif self == 'pawn' and current_square.colour == "black":
                if (int(current_square[1]) - 1) == int(new_square[1]):
                    return True
                elif (int(current_square[1]) - 1) == int(new_square[1]) \
                        and (columns[current_square[0]] - 1) == columns[new_square[0]] \
                        and self.valid_capture(current_square, new_square):
                    return True
            elif self == "king" and row_diff in {0, 1} and col_diff in {0, 1} \
                    and not new_square.under_assault(current_square.colour):
                return True
        elif self == "knight":
            if (row_diff == 1 and col_diff == 2) or (row_diff == 2 and col_diff == 1):
                return True
        else:
            return False

    def collision(self, current_square, new_square):
        columns = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        letters = "abcdefgh"
        cur_col_num = columns[current_square[0]]
        new_col_num = columns[new_square[0]]

        if current_square.piece == "knight":
            return False

        for i in range(cur_col_num, new_col_num):
            for j in range(int(current_square[1]), int(new_square[1])):
                new_cord = letters[i]+str(j)

                if new_cord.piece != "none":
                    return True
        return False



def build_board():
    columns = 'abcdefgh'
    build_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight']

    for i in range(8):
        for j in range(1, 9):
            sq = columns[i] + str(j)
            if sq[1] == '1':
                sq = GameBoard(build_pieces[i], "white", False)
            elif sq[1] == '2':
                sq = GameBoard("pawn", "white", False)
            elif sq[1] == '7':
                sq = GameBoard("pawn", "black", False)
            elif sq[1] == '8':
                sq = GameBoard(build_pieces[i], "black", False)
            else:
                sq = GameBoard("none", "none", False)


def sq_under_ass(square):
    new_list = []
    found = False
    for i in threats[square]:
        if i.colour != square.colour and not i.piece.collision(i, square) and i.piece.legal_move(square, i):
            new_list.append(i)
            if not found:
                found = True

    threats[square] = new_list

    return True if found else False


def checkmate(king_square):
    columns = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
    letters = "abcdefgh"
    cur_col_num = columns[king_square[0]]

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if not sq_under_ass(letters[cur_col_num+i] + str(int(king_square[1])+j)):
                return False
    return True


build_board()

