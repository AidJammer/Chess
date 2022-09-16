class Board:
    def __init__(self):
        self.__board_squares = [['.' for i in range(8)] for j in range(8)]

    def populate_board(self, colour):
        start_position = ['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R']

        if colour.lower() == 'black':
            self.__board_squares[0] = start_position
            self.__board_squares[7] = [i.lower() for i in start_position]
            for i in range(8):
                self.__board_squares[1][i] = 'P' # Uppercase P for white pawns
                self.__board_squares[6][i] = 'p' # Lowercase p for black pawns

        else:
            self.__board_squares[7] = start_position
            self.__board_squares[0] = [i.lower() for i in start_position]
            for i in range(8):
                self.__board_squares[6][i] = 'P' # Uppercase P for white pawns
                self.__board_squares[1][i] = 'p' # Lowercase p for black pawns

    @property
    def square_check(self, row, column):
        return self.__board_squares[row][column]

    @property
    def collision(self, row, column, new_row, new_column):
        if abs(row - new_row) == abs(column - new_column):
            for i, j in zip(range(row, new_row), range(column, new_column)):
                if self.__board_squares[i][j] != '.':
                    return True
            return False

        elif abs(row - new_row) == 0:
            for i in range(column, (new_column + 1))
                if self.__board_squares[row][i] != '.':
                    return True
            return False

        elif abs(column - new_column) == 0:
            for i in range(row, (new_row + 1))
                if self.__board_squares[i][column] != '.':
                    return True
            return False

