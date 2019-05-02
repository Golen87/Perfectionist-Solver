import collections
import colors

class Board:
	def __init__(self, new_board=None):
		if new_board:
			self.width = len(new_board[0])
			self.height = len(new_board)
			self.board = new_board

			self.tile_count = self.width * self.height
			self.lost_points = 0
			self.punishment = 0
			self.number_count = sum([
				self.board[y][x]
				for y in range(self.height)
				for x in range(self.width)
			])

	# Clones to a new board
	def create_copy(self):
		new = Board()
		new.width = self.width
		new.height = self.height
		new.board = [row[:] for row in self.board]
		new.tile_count = self.tile_count
		new.lost_points = self.lost_points
		new.punishment = self.punishment
		new.number_count = self.number_count
		return new

	def serialize(self):
		return (
			self.board,
			self.tile_count,
			self.lost_points,
			self.punishment,
			self.number_count,
		)

	def deserialize(self, board_tuple):
		self.board = board_tuple[0]
		self.tile_count = board_tuple[1]
		self.lost_points = board_tuple[2]
		self.punishment = board_tuple[3]
		self.number_count = board_tuple[4]

		self.width = len(self.board[0])
		self.height = len(self.board)

	# Pretty print board
	# Optional highlight (x,y), ...
	def print_board(self, *selected):
		lines = []
		for y in range(self.height):
			line = ''
			for x in range(self.width):
				# Set number or empty if 0
				t = self.board[y][x] or '-'
				# Right align text
				t = '{:>3}'.format(t)
				# Add color to show selected tiles
				if selected and (x,y) in selected:
					t = colors.add(t, colors.B_RED)
				line += t
			lines.append(line)
		print('\n'.join(lines))


	# Checks if position is inside board
	def is_inside(self, x, y):
		return x >= 0 and y >= 0 and x < self.width and y < self.height

	# Returns value at position
	def get_value(self, pos):
		x, y = pos
		return self.board[y][x]

	# Performs move on board
	def make_move(self, move):
		x1, y1 = move[0]
		x2, y2 = move[1]
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

			# Severely punish 1-1 moves
			if v1 == 1:
				self.punishment += 10
		else:
			self.board[y1][x1] = 0
			self.board[y2][x2] = abs(v1 - v2)
			self.lost_points += min(v1, v2)
			self.tile_count -= 1

			# Punish 1-moves
			if v1 == 1:
				self.punishment += 1

		if self.tile_count == 1:
			# Remove random number remaining
			if v1 == v2:
				for dy in range(self.height):
					for dx in range(self.width):
						if self.board[dy][dx]:
							self.lost_points += self.board[dy][dx]
							self.board[dy][dx] = 0
							self.tile_count -= 1
							return
			# Remove selected number remaining
			else:
				self.lost_points += self.board[y2][x2]
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
			for dy in range(self.height):
				for dx in range(self.width):
					if (x != dx or y != dy):
						if self.board[dy][dx] > 0:
							if not v == self.board[dy][dx] == 1:
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

		#moves = [move for move in moves if self.get_move_cost(move) < 5]
		return moves

	# Returns all available moves on the board
	def get_all_moves(self, verbose=False):
		all_moves = []
		for y in range(self.height):
			for x in range(self.width):
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