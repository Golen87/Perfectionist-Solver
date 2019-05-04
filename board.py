import collections
import colors

class Board:
	def __init__(self, new_board=None):
		if new_board:
			self.width = len(new_board[0])
			self.height = len(new_board)
			self.board = new_board

			self.tile_count = sum([
				self.board[y][x] > 0
				for y in range(self.height)
				for x in range(self.width)
			])
			self.lost_points = 0
			self.punishment = 0
			self.number_count = sum([
				self.board[y][x]
				for y in range(self.height)
				for x in range(self.width)
			])
			self.moves = []

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
		new.moves = self.moves[:]
		return new

	def hash(self):
		return hash( tuple(tuple(row) for row in self.board) )

	def serialize(self):
		return (
			self.board,
			self.tile_count,
			self.lost_points,
			self.punishment,
			self.number_count,
			self.moves,
		)

	def deserialize(self, board_tuple):
		self.board = board_tuple[0]
		self.tile_count = board_tuple[1]
		self.lost_points = board_tuple[2]
		self.punishment = board_tuple[3]
		self.number_count = board_tuple[4]
		self.moves = board_tuple[5]

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

		self.moves.append(move)

		if v1 == v2:
			self.board[y1][x1] = 0
			self.board[y2][x2] = 0
			self.tile_count -= 2
			self.number_count -= v1 + v2

			# Severely punish 1-1 moves
			if v1 == 1:
				self.punishment += 10
		else:
			self.board[y1][x1] = 0
			self.board[y2][x2] = abs(v1 - v2)
			self.lost_points += min(v1, v2)
			self.tile_count -= 1
			self.number_count -= 2 * min(v1, v2)

			# Punish 1-moves
			if v1 == 1:
				self.punishment += 1

		if self.tile_count == 1:
			# Remove random number remaining
			if v1 == v2:
				for dy in range(self.height):
					for dx in range(self.width):
						if self.board[dy][dx]:
							self.number_count -= self.board[dy][dx]
							self.lost_points += self.board[dy][dx]
							self.board[dy][dx] = 0
							self.tile_count -= 1
							return
			# Remove selected number remaining
			else:
				self.number_count -= self.board[y2][x2]
				self.lost_points += self.board[y2][x2]
				self.board[y2][x2] = 0
				self.tile_count -= 1

	# Returns positions of all numbers of a given value
	def get_number_positions(self, number):
		positions = []
		for y in range(self.height):
			for x in range(self.width):
				if self.board[y][x] == number:
					positions.append( (x,y) )
		return positions

	# Returns possible moves from x,y
	def get_moves_at(self, x, y, remove_dups=False):
		moves = []
		v = self.board[y][x]

		def dup_check(x, y, dx, dy):
			return remove_dups and self.board[y][x] == self.board[dy][dx] and (x,y) < (dx,dy)

		if v == 0:
			return None

		# Find teleporting moves
		elif v == 1 or self.tile_count <= 10:
			for dy in range(self.height):
				for dx in range(self.width):
					if (x != dx or y != dy):
						if self.board[dy][dx] > 0:
							if not dup_check(x, y, dx, dy):
								moves.append( ((x,y), (dx,dy)) )

		# Find 4 neighbouring moves
		else:
			for d in [(+1,0), (-1,0), (0,+1), (0,-1)]:
				dx = x + d[0]
				dy = y + d[1]
				while self.is_inside(dx, dy):
					if self.board[dy][dx] > 0:
						if not dup_check(x, y, dx, dy):
							moves.append( ((x,y), (dx,dy)) )
						break
					dx += d[0]
					dy += d[1]

		return moves

	# Returns all available moves on the board
	def get_all_moves(self):
		all_moves = []
		for y in range(self.height):
			for x in range(self.width):
				moves = self.get_moves_at(x, y, True)
				if moves:
					all_moves += moves
		return all_moves

	# Returns optimal moves for the end game
	def get_endgame_moves(self):
		values = [self.board[y][x] for x in range(self.width) for y in range(self.height)]
		value_count = {v: values.count(v) for v in values}

		max_value = 0
		for number in range(15,0,-1):
			if value_count.get(number, 0) % 2 != 0:
				max_value = number
				break

		#remaining = []
		for number in range(15,0,-1):
			count = value_count.get(number, 0)
			if 2*number >= max_value:
				if count >= 2:
					p1, p2 = self.get_number_positions(number)[:2]
					return [(p1, p2)]
				#if count % 2 != 0:
				#	remaining.append(number)
			#else:
			#	remaining += [number] * count

		return self.get_all_moves()

	# Returns moves to be searched on the board
	def get_search_moves(self):
		if self.tile_count > 10:
			all_moves = self.get_all_moves()
		else:
			all_moves = self.get_endgame_moves()

		#lowest_cost = 15
		#for move in all_moves:
		#	lowest_cost = min(lowest_cost, self.get_move_cost(move))
		#all_moves = [move for move in all_moves if self.get_move_cost(move) <= lowest_cost + 0]
		#all_moves = all_moves[:2]
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

	# Returns the minimum remaining cost, if all tiles were magically aligned
	def get_heuristic(self):
		# Not admissible, but very fast
		return self.tile_count

		"""
		values = [self.board[y][x] for x in range(self.width) for y in range(self.height)]
		value_count = {v: values.count(v) for v in values}

		self.print_board()
		print()

		max_value = 0
		for number in range(15,0,-1):
			if value_count.get(number, 0) % 2 != 0:
				max_value = number
				break

		remaining = []
		for number in range(15,0,-1):
			count = value_count.get(number, 0)
			if 2*number >= max_value:
				if count % 2 != 0:
					remaining.append(number)
			else:
				remaining += [number] * count

		print(remaining)
		exit()
		"""

		"""
		values = [self.board[y][x] for x in range(self.width) for y in range(self.height)]
		values.sort(reverse=True)
		prev = None
		lost = 0
		for value in values:
			if prev is None:
				prev = value
			else:
				lost += prev - value
				prev = None
		if prev:
			lost += prev

		return lost + self.lost_points
		"""