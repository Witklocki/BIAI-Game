import numpy as np
import piece


class BoardState:
    def __init__(self, size, values=None, evals=None, color=piece.WHITE):
        if np.all(values != None):
            self.values = np.copy(values)
        else:
            self.values = np.full((size, size), piece.EMPTY)

        self.size = size
        self.color = color
        self.last_move = None
        self.winner = 0

    def value(self, position):
        return self.values[position]

    def isValidPosition(self, position):
        return (isValidPosition(self.size, position)
                and self.values[position] == piece.EMPTY)

    def legalMoves(self):
        prev_move_idxs = self.values != piece.EMPTY
        area_idxs = expandArea(self.size, prev_move_idxs)
        return np.column_stack(np.where(area_idxs == True))

    def next(self, position):
        next_state = BoardState(size=self.size,
                                values=self.values,
                                color=-self.color)
        next_state[position] = next_state.color
        next_state.last_move = tuple(position)
        return next_state

    def isTerminal(self):
        is_win, color = self.checkFiveInRow()
        is_full = self.isFull()
        if is_full:
            return True
        return is_win

    def checkFiveInRow(self):
        pattern = np.full((5,), 1)

        black_win = self.checkPattern(pattern * piece.BLACK)
        white_win = self.checkPattern(pattern * piece.WHITE)

        if black_win:
            self.winner = piece.BLACK
            return True, piece.BLACK
        if white_win:
            self.winner = piece.WHITE
            return True, piece.WHITE
        return False, piece.EMPTY

    def isFull(self):
        return not np.any(self.values == piece.EMPTY)

    def checkPattern(self, pattern):
        count = 0
        for line in self.getLines():
            if isSub(line, pattern):
                count += 1
        return count

    def getLines(self):
        l = []

        # rows and cols
        for i in range(self.size):
            l.append(self.values[i, :])
            l.append(self.values[:, i])

        # 2 diags
        for i in range(-self.size + 5, self.size - 4):
            l.append(np.diag(self.values, k=i))
            l.append(np.diag(np.fliplr(self.values), k=i))

        for line in l:
            yield line

    def __getitem__(self, position):
        i, j = position
        return self.values[i, j]

    def __setitem__(self, position, value):
        i, j = position
        self.values[i, j] = value

    def __str__(self):
        out = ' ' * 3
        out += '{}\n'.format(''.join(
            '{}{}'.format((i + 1) % 10, i < 10 and ' ' or "'")
            for i in range(self.size)
        ))

        for i in range(self.size):
            out += '{}{} '.format(i + 1 < 10 and ' ' or '', i + 1)
            for j in range(self.size):
                out += piece.symbols[self[i, j]]
                if self.last_move and (i, j) == tuple(self.last_move):
                    out += '*'
                else:
                    out += ' '
            if i == self.size - 1:
                out += ''
            else:
                out += '\n'
        return out

    def __repr__(self):
        return self.__str__()


def isSub(l, subl):
    l_size = len(l)
    subl_size = len(subl)
    for i in range(l_size - subl_size):
        curr = l[i:min(i + subl_size, l_size - 1)]
        if (curr == subl).all():
            return True
    return False


def expandArea(size, idxs):
    area_idxs = np.copy(idxs)
    for i in range(size):
        for j in range(size):
            if not idxs[i, j]:
                continue
            for direction in ((1, 0), (0, 1), (1, 1), (1, -1)):
                di, dj = direction
                for side in (1, -1):
                    ni = i + di * side
                    nj = j + dj * side
                    if not isValidPosition(size, (ni, nj)):
                        continue
                    area_idxs[ni, nj] = True
    return np.bitwise_xor(area_idxs, idxs)


def isValidPosition(board_size, position):
    i, j = position
    return i >= 0 and i < board_size and j >= 0 and j < board_size
