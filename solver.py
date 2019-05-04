from board import Board
import colors
import sys, heapq, pprint, importlib


def print_solution(board, moves):
	new_board = board.create_copy()
	for move in moves:
		new_board.print_board(*move)
		new_board.make_move(move)
		print('-'*new_board.width*3, new_board.lost_points)

def debug_print(board, moves, queue, show=True):
	l = board.lost_points
	p = board.punishment
	h = board.get_heuristic()

	if show:
		board.print_board()
	print('-'*board.width*3, "Cost:{} ({}/{}) Mov:{} Que:{}".format(
		l+h, l, h, len(moves), len(queue)
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
	heapq.heappush(queue, (0, 0, board.serialize()))
	visited = set()
	iterations = 0
	lowest_score = 1000

	while queue:
		lost_points, current_hash, current_board_tuple = heapq.heappop(queue)
		if current_hash in visited:
			continue
		visited.add(current_hash)

		current_board = Board()
		current_board.deserialize(current_board_tuple)
		moves = current_board.get_search_moves()

		# Check if board is complete
		if current_board.tile_count == 0 and current_board.lost_points < lowest_score:
			lowest_score = current_board.lost_points
			debug_print(current_board, moves, queue)
			pprint.pprint(current_board.moves)
			print(colors.add("Victory!", colors.B_YEL), current_board.lost_points)
			print()
			#solver.print_solution(board, current_board.moves)
			visited.remove(current_hash)
			continue

		# Occasional debug printing
		iterations += 1
		if iterations % 1000 == 0:
			debug_print(current_board, moves, queue)

		# Add all possible moves to the queue
		for move in moves:
			next_board = current_board.create_copy()
			next_board.make_move(move)

			# Cost calculations
			lost_points = next_board.lost_points
			lost_points += next_board.get_heuristic()
			#lost_points += next_board.punishment

			next_hash = next_board.hash()
			if next_hash not in visited:
				heapq.heappush(queue, (lost_points, next_hash, next_board.serialize()))



if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("python3 solver.py examples/example_X.py")
		exit()

	path = sys.argv[1].replace('/', '.').replace('.py', '')
	example = importlib.import_module(path)
	board = Board(example.board)

	print(colors.add("Start position:", colors.B_GRE))
	debug_print(board, [], [])
	print()

	#print_solution(board, example.good_solution)
	solve_with_dijkstra(board)
