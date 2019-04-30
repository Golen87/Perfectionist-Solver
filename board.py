'''A representation of the board with functions to manipulate it.'''
from __future__ import print_function

import collections
import copy

Board = collections.namedtuple(
    'Board', 'board moves points_on_board total_points lost_points pieces_left'
)


def create_board(board, moves=None, points_on_board=None, total_points=0,
                 lost_points=0, pieces_left=None):
    '''Creates a board.'''
    if points_on_board is None:
        points_on_board = sum(cell for cell in row for row in board)
    total_points = max(total_points, points_on_board)
    if pieces_left is None:
        pieces_left = sum(1 for cell in row for row in board if cell > 0)
    if moves is None:
        moves = tuple()
    return Board(board, moves, points_on_board, total_points, lost_points, pieces_left)


def create_next_board_from_move(board, move):
    '''Starts with a board and create a new board from a certain move.'''
    r1, c1, v1, r2, c2, v2 = move
    res = abs(v1 - v2)

    next_board = copy.deepcopy(board.board)
    next_board[r1][c1] = 0
    next_board[r2][c2] = res
    next_moves = board.moves + (move,)
    next_points_on_board = board.points_on_board - v1 - v2 + res
    next_lost_points = board.lost_points + \
        int(res == 0) * (v1 + v2 - res)
    removed_pieces = 1 + int(res == 0)
    next_pieces_left = board.pieces_left - removed_pieces
    return create_board(next_board, next_moves, next_points_on_board, board.total_points,
                        next_lost_points, next_pieces_left)


def print_board(board):
    '''Prints a board.'''
    for row in board:
        replaced = [' ' if cell == 0 else cell for cell in row]
        print(' '.join(replaced))


Move = collections.namedtuple(
    'Move', 'r1 c1 v1 r2 c2 v2'
)


def create_move(row1, col1, value1, row2, col2, value2):
    '''Creates a move.'''
    return Move(row1, col1, value1, row2, col2, value2)


def create_move_from_board(board, row1, col1, row2, col2):
    '''Creates a move from a board.'''
    return Move(row1, col1, board.board[row1][col1],
                row2, col2, board.board[row2][col2])
