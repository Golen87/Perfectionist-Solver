'''Dijkstra solution for perfectionist game.'''

from board import Board
import example_1, example_2, example_3
import heapq
import time

"""
def solve_less_than_10_board(board):
	'''Solves a board with less than 10 pieces left.'''
	return

def get_heuristics_move_for_board(board):
	'''A function that returns moves for a board according to clever heauristics.'''
	# TODO(Use smart heuristics here...)
	return []

def get_every_move_for_board(board):
	'''Returns every move of a board.'''
	# TODO(Maybe implement? Not sure if worth it...)
	return []

def get_moves_for_board(board):
	'''Returns the moves for a board.'''
	# Here we will need to do some form of heauristics, anything else is simply
	# not going to work. Getting every move is too damn expensive....

	#return get_heuristics_move_for_board(board)
	return get_every_move_for_board(board)
"""

def get_initial_hash():
	'''Returns the initial rolling hash.'''
	return 0

def serialize_move(move):
	'''Serializes a move.'''
	return hash(move)


LARGE_PRIME = 2**61 - 1
def update_hash(current_hash, move):
	'''Returns the updated rolling hash from the given move.'''
	return (current_hash + serialize_move(move)) % LARGE_PRIME


def debug_print(board, moves, queue, show=True):
	l = board.lost_points
	p = board.punishment
	g = board.get_heuristic()

	if show:
		board.print_board()
	print('-'*board.width*3, "Bad:{} ({}/{}/{}) Mov:{} Que:{}".format(
		l+p+g, l, p, g, len(moves), len(queue)
	))
	if show:
		print()

def solve_with_dijkstra(board):
	'''Solves using Dijkstras algorithm.

	The algorithm is based around the observation that we can traverse the
	solution of boards in order of increasing number of lost points (so first
	we solve it for 0 points, failing that we solve it for 1 point lost etc...).

	Once we find ***A*** solution (not every, just a solution), we have found
	one that is part of the set of best solutions. In order to speed it up we
	use a rolling hash over the list of moves we have produced to identify
	common states (instead of comparing board states), togehter with the number
	of lost points.

	'''
	queue = []
	heapq.heapify(queue)
	heapq.heappush(queue, (0, get_initial_hash(), board.serialize()))
	visited = set()
	iterations = 0

	while queue:
		lost_points, current_hash, current_board_tuple = heapq.heappop(queue)
		if current_hash in visited:
			continue
		visited.add(current_hash)

		current_board = Board()
		current_board.deserialize(current_board_tuple)
		moves = current_board.get_search_moves()

		if current_board.tile_count == 0:
			debug_print(current_board, moves, queue)
			print("Victory!", current_board.lost_points)
			break

		#if current_board.pieces_left <= 10:
		#	solve_less_than_10_board(board)
		#	continue

		iterations += 1
		if iterations % 100 == 0:
			debug_print(current_board, moves, queue)

		for move in moves:
			next_board = current_board.create_copy()
			next_board.make_move(move)

			lost_points = next_board.lost_points + next_board.get_heuristic() + next_board.punishment
			#next_hash = update_hash(current_hash, move)
			next_hash = next_board.hash()
			if next_hash not in visited:
				heapq.heappush(queue, (lost_points, next_hash, next_board.serialize()))


if __name__ == "__main__":
	board = Board(example_1.board)
	solve_with_dijkstra(board)