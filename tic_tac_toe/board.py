# Created as part of tic-tac-toe game
# Including representation of the Board and the Position


class GameBoard:
    """
    Represents tic-tac-toe game board
    """

    EMPTY = '-'

    def __init__(self):
        self.board = []
        for i in range(3):
            row = []
            for x in range(3):
                row.append(Position(i, x, '-'))
            self.board.append(row)
        self.last = None

    def draw(self):
        """
        Drawing a game board
        """
        view = '  0 1 2\n'
        for row in range(len(self.board)):
            view += str(row) + ' '
            for col in range(len(self.board[0])):
                view += self.board[row][col].data + ' '
            view += '\n'
        print(view)

    def _check(self, position):
        """
        Checking whether this position is part of the winning combination
        position: instance Position
        return: True, if this position is the part of winning combination
        """
        row, col = position.row, position.col

        # Possible directions
        possible = [[(0, 1), (0, -1)], [(1, 0), (-1, 0)],
                    [(-1, 1), (1, -1)], [(1, 1), (-1, -1)]]

        for var in possible:
            try:
                # Identifying row and column of neighbours
                row1, col1 = row + var[0][1], col + var[0][0]
                row2, col2 = row + var[1][1], col + var[1][0]
                if not (row1 > -1 and row2 > -1 and col1 > -1 and col2 > -1):
                    raise IndexError
                first = self.board[row1][col1]
                second = self.board[row2][col2]
                if second.data == first.data == position.data:
                    return True
            except IndexError:
                continue

    def condition(self):
        """
        return: condition of the game board, for example: Draw!
        """
        filled = 0
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                current = self.board[row][col]
                if current.data is not '-':
                    filled += 1
                    if self._check(current):
                        return current.data + ' player won'

        # Means that here are not empty places on the board
        if filled == 9:
            return 'Draw!'

    def find_empty(self):
        """
        return: coordinates of all empty positions on the board
        """
        empty = []
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                if self.board[row][column].data is self.EMPTY:
                    empty.append((row, column))
        return empty

    def add(self, row, col, data):
        """
        Changing data on position at board to given data
        row, col: position coordinates
        data: data you want to add
        """
        try:
            if self.board[row][col].data is self.EMPTY:
                self.board[row][col].data = data
                self.last = [(row, col), data]
            else:
                raise ValueError('The position is not empty')
        except IndexError:
            print('Adding on such position is not possible')


class Position:
    """
    Representing position on the game board
    """

    def __init__(self, row, col, data):
        self.row = row
        self.col = col
        self.data = data

if __name__ == '__main__':
    m = GameBoard()
    m.add(0, 0, 'X')
    m.add(1, 1, 'X')
    m.add(2, 2, 'X')
    print(m.condition())
