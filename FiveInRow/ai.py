import piece
import numpy as np
from eval_fn import *


def getBestMove(state, depth, is_max_state):
    values = state.values
    best_value = -9000 if is_max_state else 9000
    best_move = (-1, -1)
    pieces = np.count_nonzero(values != piece.EMPTY)

    if pieces == 0:
        return first(state)
    if pieces == 1:
        return second(state)

    top_moves = getMoves(state, 10, is_max_state)

    for move, value in top_moves:
        updated_state = state.next(move)
        value = minMax(updated_state, -10e5, 10e5,
                       depth - 1, not is_max_state)

        if (is_max_state and value > best_value) or (not is_max_state and value < best_value):
            best_value = value
            best_move = move

    if best_move[0] == -1 and best_move[1] == -1:
        return top_moves[0]

    return best_move, best_value


def getMoves(state, n, is_max_state):
    color = state.color
    top_moves = []

    for move in state.legalMoves():
        evaluation = statusCheck(state.next(move), color)
        top_moves.append((move, evaluation))
    return sorted(top_moves, key=lambda x: x[1], reverse=is_max_state)[:n]


def minMax(state, alpha, beta, depth, is_max_state):
    if depth == 0 or state.isTerminal():
        return statusCheck(state, -state.color)

    if is_max_state:
        value = -9000
        for move in state.legalMoves():
            value = max(
                value,
                minMax(state.next(move), alpha, beta, depth - 1, False)
            )
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return value
    else:
        value = 9000
        for move in state.legalMoves():
            value = min(
                value,
                minMax(state.next(move), alpha, beta, depth - 1, True)
            )
            beta = min(value, beta)
            if alpha >= beta:
                break
        return value


def first(state):
    x = state.size // 2
    return np.random.choice((x - 1, x, x + 1), 2), 1


def second(state):
    i, j = state.last_move
    size = state.size
    i2 = i <= size // 2 and 1 or -1
    j2 = j <= size // 2 and 1 or -1
    return (i + i2, j + j2), 2
