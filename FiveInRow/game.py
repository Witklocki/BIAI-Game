import piece
import numpy as np
from board import BoardState
from ai import *


class GameRunner:
    def __init__(self, size=13, depth=2):
        self.size = size
        self.depth = depth
        self.finished = False
        self.restart()

    def restart(self, player_index=-1):
        self.is_max_state = True if player_index == -1 else False
        self.state = BoardState(self.size)
        self.ai_color = -player_index

    def play(self, i, j):
        position = (i, j)
        if self.state.color != self.ai_color:
            return False
        if not self.state.isValidPosition(position):
            return False
        self.state = self.state.next(position)
        self.finished = self.state.isTerminal()
        return True

    def aiplay(self):
        if self.state.color == self.ai_color:
            return False, (0, 0)
        move, value = getBestMove(self.state, self.depth, self.is_max_state)
        self.state = self.state.next(move)
        self.finished = self.state.isTerminal()
        # print(time.time() - t)
        return True, move

    def getStatus(self):
        board = self.state.values
        return {
            'board': board.tolist(),
            'next': -self.state.color,
            'finished': self.finished,
            'winner': self.state.winner,
            # 'debug_board': self.state.__str__()
        }
