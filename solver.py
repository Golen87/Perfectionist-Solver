import colors
import example_1, example_2, example_3


class Board:
	def __init__(self, new_board=None):
		if new_board:
			self.WIDTH = len(new_board[0])
			self.HEIGHT = len(new_board)
			self.board = new_board

			self.tile_count = self.WIDTH * self.HEIGHT
			self.lost = 0

			"""
			self.tile_count = sum([
				self.board[y][x] > 0
				for y in range(self.HEIGHT)
				for x in range(self.WIDTH)
			])
			"""

	# Clones to a new board
	def create_copy(self):
		new = Board()
		new.WIDTH = self.WIDTH
		new.HEIGHT = self.HEIGHT
		new.board = [row[:] for row in self.board]
		new.tile_count = self.tile_count
		new.lost = self.lost
		return new

	def get_hash(self):
		...


	# Pretty print board
	# Optional highlight (x,y), ...
	def print_board(self, *selected):
		lines = []
		for y in range(self.HEIGHT):
			line = ''
			for x in range(self.WIDTH):
				# Set number or empty if 0
				t = self.board[y][x] or '-'
				# Right align text
				t = f'{t:>3}'
				# Add color to show selected tiles
				if selected and (x,y) in selected:
					t = colors.add(t, colors.B_RED)
				line += t
			lines.append(line)
		print('\n'.join(lines))


	# Checks if position is inside board
	def is_inside(self, x, y):
		return x >= 0 and y >= 0 and x < self.WIDTH and y < self.HEIGHT

	# Returns value at position
	def get_value(self, pos):
		x, y = pos
		return self.board[y][x]

	# Performs move on board
	def make_move(self, posFrom, posTo):
		x1, y1 = posFrom
		x2, y2 = posTo
		v1 = self.board[y1][x1]
		v2 = self.board[y2][x2]

		if x1 != x2 and y1 != y2 and v1 != 1 and self.tile_count > 10:
			raise Exception("Invalid move (not aligned)")
		if v1 == 0 or v2 == 0:
			raise Exception("Invalid move (zero)")

		if v1 == v2:
			self.board[y1][x1] = 0
			self.board[y2][x2] = 0
			self.tile_count -= 2
		else:
			self.board[y1][x1] = 0
			self.board[y2][x2] = abs(v1 - v2)
			self.lost += min(v1, v2)
			self.tile_count -= 1

		if self.tile_count == 1:
			# Remove random number remaining
			if v1 == v2:
				for dy in range(self.HEIGHT):
					for dx in range(self.WIDTH):
						if self.board[dy][dx]:
							self.lost += self.board[dy][dx]
							self.board[dy][dx] = 0
							self.tile_count -= 1
							return
			# Remove selected number remaining
			else:
				self.lost += self.board[y2][x2]
				self.board[y2][x2] = 0
				self.tile_count -= 1

	# Returns possible moves from x,y
	def get_moves_at(self, x, y, verbose):
		moves = []
		v = self.board[y][x]

		if v == 0:
			return None

		# Find teleporting moves
		elif v == 1 or self.tile_count <= 10:
			for dy in range(self.HEIGHT):
				for dx in range(self.WIDTH):
					if (x != dx or y != dy) and self.board[dy][dx] > 0:
						moves.append( ((x,y), (dx,dy)) )

		# Find 4 neighbouring moves
		else:
			for d in [(+1,0), (-1,0), (0,+1), (0,-1)]:
				dx = x + d[0]
				dy = y + d[1]
				while self.is_inside(dx, dy):
					if self.board[dy][dx] > 0:
						moves.append( ((x,y), (dx,dy)) )
						break
					dx += d[0]
					dy += d[1]

		return moves

	# Returns all available moves on the board
	def get_all_moves(self, verbose=False):
		all_moves = []
		for y in range(self.HEIGHT):
			for x in range(self.WIDTH):
				moves = self.get_moves_at(x, y, verbose)
				if moves:
					all_moves += moves
		return all_moves

	# Returns cost of a move
	def get_move_cost(self, move):
		x1, y1 = move[0]
		x2, y2 = move[1]
		v1 = self.board[y1][x1]
		v2 = self.board[y2][x2]

		if v1 == v2:
			return 0
		return min(v1, v2)



board = Board(example_1.board)

def cheat_solve():
	sol = example_1.good_solution
	while sol:
		move = sol.pop(0)
		board.print_board(*move)
		board.make_move(*move)
		print('-'*board.WIDTH*3, board.lost)

def greedy_solve():
	while board.tile_count > 0:
		moves = board.get_all_moves()
		# Sort by lowest cost, highest value
		moves.sort(key=lambda move: (board.get_move_cost(move), -board.get_value(move[0])))
		move = moves[0]

		board.print_board(*move)
		board.make_move(*move)
		print('-'*board.WIDTH*3, board.lost)

#cheat_solve()
greedy_solve()
