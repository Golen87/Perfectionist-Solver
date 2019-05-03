import colors
import example_1, example_2, example_3, example_4
from board import Board

board = Board(example_4.board)

def cheat_solve():
	sol = example_4.good_solution
	while sol:
		move = sol.pop(0)
		board.print_board(*move)
		board.make_move(move)
		print('-'*board.width*3, board.lost_points)

def greedy_solve():
	while board.tile_count > 0:
		moves = board.get_all_moves()
		# Sort by lowest cost, highest value
		moves.sort(key=lambda move: (board.get_move_cost(move), -board.get_value(move[0])))
		move = moves[0]

		board.print_board(*move)
		board.make_move(move)
		print('-'*board.width*3, board.lost_points)

def greedy_depth_solve():
	def get_best_move(board, depth=0):
		moves = board.get_all_moves()
		if not moves:
			return None, (0,0,0,0)

		scoring = []
		for move in moves:
			temp = board.create_copy()
			temp.make_move(move)
			move_costs = [temp.get_move_cost(m) for m in temp.get_all_moves()]
			mincost = -1 if not move_costs else min(move_costs)

			score = (
				mincost,
				temp.lost_points,
				-move_costs.count(mincost),
				-max(temp.get_value(move[0]), temp.get_value(move[1]))
			)

			scoring.append((
				move,
				score
			))

		# Reevaluate score
		if depth == 0:
			scoring.sort(key=lambda x:x[1])
			for i in range(len(scoring[:0])):
				move = scoring[i][0]
				temp = board.create_copy()
				temp.make_move(move)
				best = get_best_move(temp, depth+1)
				if best[1] < scoring[i][1]:
					print("Better!", best[1], scoring[i][1])
					scoring[i] = (scoring[i][0], best[1])
				else:
					print("Worse...", best[1], scoring[i][1])
		scoring.sort(key=lambda x:x[1])
		best = scoring[0]

		if depth == 0:
			return best[0]
		else:
			return best

	while board.tile_count > 0:
		move = get_best_move(board)
		board.print_board(*move)
		board.make_move(move)
		print('-'*board.width*3, board.lost_points)

if __name__ == "__main__":
	cheat_solve()
	#greedy_solve()
	#greedy_depth_solve()
